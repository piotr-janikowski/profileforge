from fastapi import FastAPI
from app.schemas.ingest_schema import RawProfileIn
from app.api.routes_profiles import router as profiles_router
from app.api.routes_ingest import router as ingest_router
from app.core.exceptions import global_exception_handler

app = FastAPI()

app.include_router(profiles_router)
app.include_router(ingest_router)

app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health")
def health_check():
    return {"status": "ok"}