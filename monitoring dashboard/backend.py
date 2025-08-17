from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql+psycopg2://postgres:gouru%402025@localhost/monitoring_dashboard"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MachineData(Base):
    __tablename__ = "machine_data"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer)
    name = Column(String)
    status = Column(String)
    production_count = Column(Integer)
    temperature = Column(Float)
    energy = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Enable CORS so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for more safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/machine-data")
async def receive_machine_data(request: Request):
    data = await request.json()
    db = SessionLocal()
    try:
        record = MachineData(
            machine_id=data["machine_id"],
            name=data["name"],
            status=data["status"],
            production_count=data["production_count"],
            temperature=data["temperature"],
            energy=data["energy"],
            timestamp=datetime.datetime.fromtimestamp(data["timestamp"])
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    finally:
        db.close()
    print("Received and stored data:", data)
    return {"status": "success"}

@app.get("/machine-data-latest")
def get_latest_machine_data():
    db = SessionLocal()
    try:
        records = db.query(MachineData).order_by(MachineData.timestamp.desc()).limit(10).all()
        return [
            {
                "machine_id": r.machine_id,
                "name": r.name,
                "status": r.status,
                "production_count": r.production_count,
                "temperature": r.temperature,
                "energy": r.energy,
                "timestamp": r.timestamp.isoformat()
            }
            for r in records
        ]
    finally:
        db.close()
