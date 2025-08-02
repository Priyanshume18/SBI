# 💼 SBI Hackathon 2025 – Intelligent Loan Risk & Tracking System

A modular system designed for SBI to tackle fraud detection, last-known location tracking of defaulters, and loan approval risk assessment.

---

## 📁 Folder Structure

<pre> . ├── DB_api/ │ └── fast_api/ # Backend for CSV-based defaulter prediction & loan approval │ └── sbi/ │ └── venv311/ # Python 3.11 virtual environment ├── ps1/ # Task 1: Fraud/defaulter prediction solution (model + CSV) ├── sbi-vishnu/ │ └── sbi-prototype1/ # Frontend + FastAPI for last known location prediction ├── sbitest.ipynb # Jupyter notebook for Task 1 model inference └── README.md # You're reading it! </pre>

## 🚀 How to Run the System

This project contains multiple components across different folders. Follow the steps below:

---

### 🔑 1. Setup SBI Login & Frontend Interface

- Navigate to:
cd sbi-vishnu/sbi-prototype1/

- Run the frontend:
npm install
npm run dev

- The frontend will be live at `http://localhost:5173/` (default Vite port)

---

### 🧠 2. Start the API for Last Known Location (GNN/LSTM-based)

- Navigate inside the same `sbi-prototype1` folder to find the FastAPI code.
- Run the FastAPI server:
uvicorn app:app --reload --port 9000

---

### 📄 3. Start the API for CSV Prediction + Loan Approval

- Navigate to:
cd DB_api/fast_api/
- Activate the virtual environment:
cd sbi/venv311/
.\Scripts\activate # On Windows

- Run both FastAPI apps on different ports (e.g., 8000 and 8001):
uvicorn sbi.load_data:app --reload --port 8000 # For loading data
uvicorn sbi.csv_predict:app --reload --port 8001 # For CSV defaulter prediction
---

### 📊 4. Model Prediction (PS1) - Optional Local Testing

For Task 1 fraud prediction using a test dataset:

- Run the notebook:
sbitest.ipynb
- Or use the standalone script inside `/ps1/`

---

## 🧪 Tech Stack

- **Frontend:** React (Vite), Tailwind CSS
- **Backend:** Python FastAPI, Uvicorn
- **ML Models:** LSTM, GNN, XGBoost (Many more)
- **Others:** Google Maps API, JWT Auth, SHAP (for explainability)

---

## 📌 Notes

- Make sure all three FastAPI servers (9000, 8000, 8001) are running for full functionality.
- The system is modular and currently not packaged into a single monorepo. Each folder runs independently.
- You may need to configure CORS headers in the backend APIs to allow frontend access.

---

## 📬 Contact

For queries, feel free to reach out via this repo or contact [Priyanshu Maurya(priyanshuiitg2026@gmail.com)] – Team Leader Idaten, SBI Hackathon
