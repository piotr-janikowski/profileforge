from app.database.session import SessionLocal
from app.models.profile_model import Profile
from app.services.entity_resolution import find_matching_profile, merge_profiles

def test_find_matching_profile_by_email():
    db = SessionLocal()

    try:
        # Arrange
        profile = Profile(
            first_name="Jan",
            last_name="Kowalski",
            age=30,
            phone_number="501234567",
            email="jan@example.com",
            address="Wroclaw",
            comment=None,
            source="test",
        )

        db.add(profile)
        db.flush()

        # Act
        result = find_matching_profile(
            db=db,
            email="jan@example.com",
            phone_number=None,
            first_name="Someone",
            last_name="Else",
        )

        # Assert
        assert result is profile

    finally:
        db.rollback()
        db.close()


def test_find_matching_profile_by_phone():
    db = SessionLocal()

    try:
        # Arrange
        profile = Profile(
            first_name="Jan",
            last_name="Kowalski",
            age=30,
            phone_number="501234567",
            email=None,
            address="Wroclaw",
            comment=None,
            source="test",
        )

        db.add(profile)
        db.flush()

        # Act
        result = find_matching_profile(
            db=db,
            email=None,
            phone_number="501234567",
            first_name="Someone",
            last_name="Else",
        )

        # Assert
        assert result is profile

    finally:
        db.rollback()
        db.close()


def test_find_matching_profile_by_fuzzy_name():
    db = SessionLocal()

    try:
        # Arrange
        profile = Profile(
            first_name="Jan",
            last_name="Kowalsky",
            age=30,
            phone_number=None,
            email=None,
            address="Wroclaw",
            comment=None,
            source="test",
        )

        db.add(profile)
        db.flush()

        # Act
        result = find_matching_profile(
            db=db,
            email=None,
            phone_number=None,
            first_name="Jan",
            last_name="Kowalski",
        )

        # Assert
        assert result is profile

    finally:
        db.rollback()
        db.close()


def test_find_matching_profile_below_similarity_threshold():
    db = SessionLocal()

    try:
        # Arrange
        profile = Profile(
            first_name="Piotr",
            last_name="Nowak",
            age=30,
            phone_number=None,
            email=None,
            address="Wroclaw",
            comment=None,
            source="test",
        )

        db.add(profile)
        db.flush()

        # Act
        result = find_matching_profile(
            db=db,
            email=None,
            phone_number=None,
            first_name="Jan",
            last_name="Kowalski",
        )

        # Assert
        assert result is None

    finally:
        db.rollback()
        db.close()


def test_find_matching_profile_returns_none_when_no_match():
    db = SessionLocal()

    try:
        # Arrange
        profile = Profile(
            first_name="Jan",
            last_name="Kowalski",
            age=30,
            phone_number="501234567",
            email="jan@example.com",
            address="Wroclaw",
            comment=None,
            source="test",
        )

        db.add(profile)
        db.flush()

        # Act
        result = find_matching_profile(
            db=db,
            email="different@example.com",
            phone_number="601234567",
            first_name="Piotr",
            last_name="Nowak",
        )

        # Assert
        assert result is None

    finally:
        db.rollback()
        db.close()


def test_merge_profiles_fills_missing_values():
    # Arrange
    existing_profile = Profile(
        first_name="Jan",
        last_name="Kowalski",
        age=None,
        phone_number=None,
        email=None,
        address="Wroclaw",
        comment=None,
        source="test",
    )

    new_profile = {
        "first_name": "John",
        "last_name": "Smith",
        "age": 30,
        "phone_number": "501234567",
        "email": "jan@example.com",
        "address": "Warsaw",
        "comment": "New comment",
        "source": "new_source",
    }

    # Act
    result = merge_profiles(existing_profile, new_profile)

    # Assert
    assert result.age == 30
    assert result.phone_number == "501234567"
    assert result.email == "jan@example.com"
    assert result.comment == "New comment"

    # Existing values should remain unchanged
    assert result.first_name == "Jan"
    assert result.last_name == "Kowalski"
    assert result.address == "Wroclaw"
    assert result.source == "test"


def test_merge_profiles_does_not_overwrite_existing_values():
    # Arrange
    existing_profile = Profile(
        first_name="Jan",
        last_name="Kowalski",
        age=30,
        phone_number="501234567",
        email="old@example.com",
        address="Wroclaw",
        comment="Old comment",
        source="old_source",
    )

    new_profile = {
        "first_name": "John",
        "last_name": "Smith",
        "age": 40,
        "phone_number": "601234567",
        "email": "new@example.com",
        "address": "Warsaw",
        "comment": "New comment",
        "source": "new_source",
    }

    # Act
    result = merge_profiles(existing_profile, new_profile)

    # Assert
    assert result.first_name == "Jan"
    assert result.last_name == "Kowalski"
    assert result.age == 30
    assert result.phone_number == "501234567"
    assert result.email == "old@example.com"
    assert result.address == "Wroclaw"
    assert result.comment == "Old comment"
    assert result.source == "old_source"


def test_merge_profiles_does_not_replace_values_with_none():
    # Arrange
    existing_profile = Profile(
        first_name="Jan",
        last_name="Kowalski",
        age=30,
        phone_number="501234567",
        email="jan@example.com",
        address="Wroclaw",
        comment="Existing comment",
        source="test",
    )

    new_profile = {
        "first_name": None,
        "last_name": None,
        "age": None,
        "phone_number": None,
        "email": None,
        "address": None,
        "comment": None,
        "source": None,
    }

    # Act
    result = merge_profiles(existing_profile, new_profile)

    # Assert
    assert result.first_name == "Jan"
    assert result.last_name == "Kowalski"
    assert result.age == 30
    assert result.phone_number == "501234567"
    assert result.email == "jan@example.com"
    assert result.address == "Wroclaw"
    assert result.comment == "Existing comment"
    assert result.source == "test"