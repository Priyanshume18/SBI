from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from pydantic import BaseModel

import pandas as pd
import numpy as np
import pickle

# -------------------- Initialize FastAPI with CORS -------------------- #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:3000"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Load LSTM Model -------------------- #
from tensorflow.keras.models import load_model
from tensorflow.keras.initializers import Orthogonal

lstm_model = load_model("lstm_tower_predictor.h5", custom_objects={'Orthogonal': Orthogonal})
with open("lstm_label_encoder.pkl", "rb") as f:
    lstm_encoder = pickle.load(f)

# -------------------- Load GNN Model -------------------- #
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv

with open("gnn_label_encoder.pkl", "rb") as f:
    gnn_encoder = pickle.load(f)

class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GraphSAGE, self).__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
    
    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

gnn_model = GraphSAGE(2, 32, len(gnn_encoder.classes_))
gnn_model.load_state_dict(torch.load("gnn_tower_predictor.pth"))
gnn_model.eval()

# -------------------- Load Data -------------------- #
tower_logs = pd.read_csv("fake_tower_logs_with_locations.csv")
account_map = pd.read_csv("fake_account_device_mapping.csv")

# Preprocess Graph Data
tower_logs['tower_num'] = gnn_encoder.transform(tower_logs['tower_id'])
tower_features = tower_logs[['tower_num', 'latitude', 'longitude']].drop_duplicates().sort_values('tower_num')
x = torch.tensor(tower_features[['latitude', 'longitude']].values, dtype=torch.float)

edges = []
for device_id, group in tower_logs.groupby('device_id'):
    tower_seq = group.sort_values('timestamp')['tower_num'].tolist()
    edges += [(tower_seq[i], tower_seq[i+1]) for i in range(len(tower_seq)-1)]

edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
graph_data = Data(x=x, edge_index=edge_index)

# -------------------- Request Body Models -------------------- #
class LSTMInput(BaseModel):
    account_id: int

class GNNInput(BaseModel):
    account_id: int

# -------------------- Routes -------------------- #
@app.get("/")
def health_check():
    return {"status": "API running"}

@app.post("/predict/lstm")
def predict_lstm(data: LSTMInput):
    try:
        device_ids = account_map[account_map['account_id'] == data.account_id]['device_id'].values
        if len(device_ids) == 0:
            return JSONResponse(status_code=404, content={"detail": f"Account ID {data.account_id} not found"})

        device_id = device_ids[0]
        user_logs = tower_logs[tower_logs['device_id'] == device_id].sort_values('timestamp')
        sequence = user_logs['tower_id'].tolist()

        if not sequence:
            return JSONResponse(status_code=400, content={"detail": "No tower logs found for this account"})

        encoded = lstm_encoder.transform(sequence)
        padded = np.zeros((1, 5))
        padded[0, -len(encoded):] = encoded[-5:]  # right padding

        pred_idx = np.argmax(lstm_model.predict(padded, verbose=0))
        tower_id = lstm_encoder.inverse_transform([pred_idx])[0]

        return {"predicted_tower_id": tower_id}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

@app.post("/predict/gnn")
def predict_gnn(data: GNNInput):
    try:
        device_ids = account_map[account_map['account_id'] == data.account_id]['device_id'].values
        if len(device_ids) == 0:
            return JSONResponse(status_code=404, content={"detail": f"Account ID {data.account_id} not found"})

        device_id = device_ids[0]
        user_logs = tower_logs[tower_logs['device_id'] == device_id].sort_values('timestamp')

        if user_logs.empty:
            return JSONResponse(status_code=400, content={"detail": "No tower logs found for this account"})

        last_tower_id = user_logs.iloc[-1]['tower_id']
        last_tower_num = gnn_encoder.transform([last_tower_id])[0]

        out = gnn_model(graph_data.x, graph_data.edge_index)
        pred_idx = torch.argmax(out[last_tower_num]).item()
        tower_id = gnn_encoder.inverse_transform([pred_idx])[0]

        return {"predicted_tower_id": tower_id}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )
