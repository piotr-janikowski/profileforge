from datetime import datetime
from pydantic import BaseModel, Field

class ProfileCreate(BaseModel):
    first_name: str = Field(..., examples=["Michał"])
    last_name: str = Field(..., examples=["Kowalski"])
    age: int | None = Field(None, examples=[26])
    phone_number: str | None = Field(None, examples=["+48123456789"])
    email: str | None = Field(None, examples=["michal.kowalski@example.com"])
    address: str = Field(..., examples=["ul. Długa 10, 50-123 Wrocław, Poland"])
    comment: str | None = Field(None, examples=["Interested in the premium offer."])
    source: str = Field(..., examples=["website"])


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None
    comment: str | None = None
    #source: str | None = None -m "source intentionally omitted - should not be editable after creation"


class ProfileOut(BaseModel):
    id: int = Field(..., examples=[1])
    first_name: str = Field(..., examples=["Michał"])
    last_name: str = Field(..., examples=["Kowalski"])
    age: int | None = Field(None, examples=[26])
    phone_number: str | None = Field(None, examples=["+48123456789"])
    email: str | None = Field(None, examples=["michal.kowalski@example.com"])
    address: str = Field(..., examples=["ul. Długa 10, 50-123 Wrocław, Poland"])
    comment: str | None = Field(None, examples=["Interested in the premium offer."])
    source: str = Field(..., examples=["website"])
    created_at: datetime = Field(..., examples=["2026-08-19T14:30:00"])

    class Config:
        from_attributes = True  # Pozwóla Pydantic tworzyć model z obiektu SQLAlchemy przez jego pola/atrybuty. Bez tego return często nie działa z response_model=ProfileOut w FastAPI, bo Pydantic nie wie jak zmapować obiekt SQLAlchemy na model Pydantic. 