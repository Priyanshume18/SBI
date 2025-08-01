import pandas as pd
from db import SessionLocal
from models import LoanAccount
from models import Base
from db import engine

Base.metadata.create_all(bind=engine)

df = pd.read_csv("target_balanced_20.csv")
df = df.dropna()  # Optional: drop rows with missing values

db = SessionLocal()
for _, row in df.iterrows():
    record = LoanAccount(**row.to_dict())
    db.add(record)

db.commit()
db.close()
