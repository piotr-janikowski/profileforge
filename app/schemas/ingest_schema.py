from pydantic import BaseModel

class RawProfileIn(BaseModel):
    name: str
    age: str
    phone_number: str | None = None
    email: str | None = None
    address: str
    comment: str | None = None
    source: str
    created_at: str