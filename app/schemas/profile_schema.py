from datetime import datetime
from pydantic import BaseModel

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    age: int | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str
    comment: str | None = None
    source: str

class ProfileOut(BaseModel):    #Zwracanie danych po utworzeniu profilu / zwracanie profilu z GET /profiles
    id: int
    first_name: str
    last_name: str
    age: int | None
    phone_number: str | None
    email: str | None
    address: str
    comment: str | None
    source: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pozwóla Pydantic tworzyć model z obiektu SQLAlchemy przez jego pola/atrybuty. Bez tego return często nie działa z response_model=ProfileOut w FastAPI, bo Pydantic nie wie jak zmapować obiekt SQLAlchemy na model Pydantic. 