from pydantic import BaseModel, Field
from datetime import datetime

class RawProfileIn(BaseModel):
    name: str = Field(..., examples=["Michał Kowalski"])
    age: str = Field(..., examples=["26 lat"])
    phone_number: str | None = Field(None, examples=["+48 123 456 789"])
    email: str | None = Field(None, examples=["michal.kowalski@example.com"])
    address: str = Field(..., examples=["ul. Długa 10, 50-123 Wrocław, Poland"])
    comment: str | None = Field(None, examples=["Interested in the premium offer."])
    source: str = Field(..., examples=["website"])