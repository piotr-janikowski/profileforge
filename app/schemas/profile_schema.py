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

class ProfileOut(BaseModel):
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
        orm_mode = True