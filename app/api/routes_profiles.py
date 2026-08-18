from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.profile_schema import ProfileCreate, ProfileOut, ProfileUpdate
from app.services import profile_service

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileOut, status_code=201)    # Messy data from external sources requires deduplication, while POST /profiles represents a workflow in which someone (e.g. through an administrative panel) intentionally creates a single, specific, already-clean profile.
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    return profile_service.create_profile(db, data)


@router.put("/{profile_id}", response_model=ProfileOut)
def update_profile(profile_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    updated = profile_service.update_profile(db, profile_id, data.model_dump(exclude_unset=True))   # .model_dump(exclude_unset=True) zwraca tylko pola, które użytkownik podał. Gdyby było False to zwróciłby wszystkie niewypełnione jako None
    if updated is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated


@router.delete("/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    deleted = profile_service.delete_profile(db, profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Profile not found")
    return Response(status_code=204)


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = profile_service.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/", response_model=list[ProfileOut])
def list_profiles(skip: int = 0, limit: int = 20, email: str | None = None, source: str | None = None, db: Session = Depends(get_db)):
    return profile_service.list_profiles(db, skip, limit, email, source)