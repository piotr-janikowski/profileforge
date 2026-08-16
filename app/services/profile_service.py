from sqlalchemy.orm import Session
from app.models.profile_model import Profile
from app.schemas.profile_schema import ProfileCreate

def create_profile(db: Session, data: ProfileCreate) -> Profile:
    new_profile = Profile(**data.model_dump())  # **unpack the dictionary into keyword arguments and .model_dump() is used to convert the Pydantic model into a dictionary
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


def save_profile(db: Session, profile: Profile) -> Profile:
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, profile_id: int) -> Profile | None:
    return db.query(Profile).filter(Profile.id == profile_id).first()


def list_profiles(db: Session, skip: int = 0, limit: int = 20) -> list[Profile]:
    return db.query(Profile).offset(skip).limit(limit).all()