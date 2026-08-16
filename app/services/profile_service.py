from sqlalchemy.orm import Session
from app.models.profile_model import Profile
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate


# Creat new profile
def create_profile(db: Session, data: ProfileCreate) -> Profile:
    new_profile = Profile(**data.model_dump())  # **unpack the dictionary into keyword arguments and .model_dump() is used to convert the Pydantic model into a dictionary
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# Update existing profile
def update_profile(db: Session, profile_id: int, data: dict) -> Profile | None:
    profile = get_profile(db, profile_id)
    if profile is None:
        return None 

    for key, value in data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


# Delete profile - po delete nie ma refresh
def delete_profile(db: Session, profile_id: int) -> bool:
    profile = get_profile(db, profile_id)
    if profile is None:
        return False

    db.delete(profile)
    db.commit()

    return True


# Get profile
def get_profile(db: Session, profile_id: int) -> Profile | None:
    return db.query(Profile).filter(Profile.id == profile_id).first()


# List all profiles with limit and skip (pagination)
def list_profiles(
        db: Session, 
        skip: int = 0, 
        limit: int = 20, 
        email: str | None = None, 
        source: str | None = None
        ) -> list[Profile]:
    query = db.query(Profile)   #Tworzymy obiekt reprezentujący zapytanie SQL

    if email is not None:
        query = query.filter(Profile.email.ilike(f"%{email}%"))
    
    if source is not None:
        query = query.filter(Profile.source == source)

    return query.offset(skip).limit(limit).all()


def save_profile(db: Session, profile: Profile) -> Profile:
    db.commit()
    db.refresh(profile)
    return profile