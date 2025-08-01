from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import SessionLocal
from models import LoanAccount

# -------------------- FastAPI App Initialization -------------------- #
app = FastAPI()

# ✅ CORS Configuration: allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Database Dependency -------------------- #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Endpoint: Get TARGET by UNIQUE_ID -------------------- #
@app.get("/target/{unique_id}")
def get_target_by_unique_id(unique_id: int, db: Session = Depends(get_db)):
    record = db.query(LoanAccount).filter(LoanAccount.UNIQUE_ID == unique_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"UNIQUE_ID": unique_id, "TARGET": record.TARGET}
