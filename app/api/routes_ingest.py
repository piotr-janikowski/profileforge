from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.ingest_schema import RawProfileIn
from app.schemas.profile_schema import ProfileOut, ProfileCreate
from app.services.normalization import (
    normalize_name,
    split_full_name,
    normalize_phone,
    normalize_age,
    normalize_email,
    normalize_address,
    normalize_comment
    )
from app.services.entity_resolution import find_matching_profile, merge_profiles
from app.services.profile_service import save_profile, create_profile


router = APIRouter(tags=["Ingest"])


# Orchestration endpoint for ingesting raw profile data
@router.post("/ingest", response_model=ProfileOut)
def ingest(data: RawProfileIn, db: Session = Depends(get_db)):
    """Ingests a raw profile and returns the created or updated profile."""

    normalized_name = normalize_name(data.name)
    normalized_first_name, normalized_last_name = split_full_name(normalized_name)
    if not normalized_first_name and not normalized_last_name:
        raise HTTPException(status_code=422, detail={"field": "name", "message": "Name could not be parsed into first and last name"})
    normalized_phone = normalize_phone(data.phone_number)
    normalized_age = normalize_age(data.age)
    normalized_email = normalize_email(data.email)
    normalized_address = normalize_address(data.address)
    normalized_comment = normalize_comment(data.comment)

    incoming_data = {
        "first_name": normalized_first_name,
        "last_name": normalized_last_name,
        "phone_number": normalized_phone,
        "age": normalized_age,
        "email": normalized_email,
        "address": normalized_address,
        "comment": normalized_comment,
        "source": data.source
    }

    matching_profile = find_matching_profile(db, normalized_email, normalized_phone, normalized_first_name, normalized_last_name)
    if matching_profile:
        merged_profile = merge_profiles(matching_profile, incoming_data)
        return save_profile(db, merged_profile)

    profile_create = ProfileCreate(**incoming_data)
    return create_profile(db, profile_create)

