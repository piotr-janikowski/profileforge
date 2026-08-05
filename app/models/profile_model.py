from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    source = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())