from app.models.profile_model import Profile
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

def find_matching_profile(
    db: Session,
    email: str | None,
    phone_number: str | None,
    first_name: str,
    last_name: str,
    name_similarity_threshold: int = 90,
) -> Profile | None:
    """ Finds a matching profile using, in order: exact email match, exact phone match, 
    or fuzzy first+last name similarity above name_similarity_threshold. Returns None if no match is found."""

    # 1. Exact match by email
    if email is not None:
        profile = (db.query(Profile).filter(Profile.email == email).first())
        if profile is not None:
            return profile

    # 2. Exact match by phone number
    if phone_number is not None:
        profile = (db.query(Profile).filter(Profile.phone_number == phone_number).first())
        if profile is not None:
            return profile

    # 3. Fuzzy matching by first name + last name
    profiles = db.query(Profile).all()

    input_full_name = f"{first_name} {last_name}"

    best_match: Profile | None = None
    best_score = 0

    for profile in profiles:
        profile_full_name = f"{profile.first_name} {profile.last_name}"

        score = fuzz.ratio(input_full_name,profile_full_name)

        if score > best_score:
            best_score = score
            best_match = profile

    # 4. Check similarity threshold
    if best_match is not None and best_score >= name_similarity_threshold:
        return best_match

    # 5. No sufficiently good match
    return None



def merge_profiles(existing_profile: Profile, new_profile: dict) -> Profile:
    """Merge missing values from new_profile into existing_profile."""

    fields = [
        "first_name",
        "last_name",
        "age",
        "phone_number",
        "email",
        "address",
        "comment",
        "source",
    ]

    for field in fields:
        existing_value = getattr(existing_profile, field)
        new_value = new_profile.get(field)

        if existing_value is None and new_value is not None:
            setattr(existing_profile, field, new_value)

    return existing_profile