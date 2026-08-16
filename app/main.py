from fastapi import FastAPI
from app.schemas.ingest_schema import RawProfileIn
from app.api.routes_profiles import router as profiles_router
from app.api.routes_ingest import router as ingest_router

app = FastAPI()

app.include_router(profiles_router)
app.include_router(ingest_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(data: RawProfileIn):
    return data