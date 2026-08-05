from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.profile_schema import ProfileCreate, ProfileOut
from app.services import profile_service

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileOut)
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    return profile_service.create_profile(db, data)


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = profile_service.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/", response_model=list[ProfileOut])
def list_profiles(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return profile_service.list_profiles(db, skip, limit)