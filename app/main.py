from fastapi import FastAPI
from app.schemas.ingest_schema import RawProfileIn

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(data: RawProfileIn):
    return data