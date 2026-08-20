from app.models.profile_model import Profile

def test_ingest_creates_new_profile(client, db_session): # Pytest sam rozpozna te nazwy jako fixture'y z conftest.py i je wywoła, w odpowiedniej kolejności
    payload = {
        "name": "Michał Kowalski",
        "age": "26",
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": "",
        "source": "web_form",
    }

    response = client.post("/ingest", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Michał"
    assert data["last_name"] == "Kowalski"
    assert data["age"] == 26
    assert data["phone_number"] == "+48123456789"
    assert data["email"] == "michal@example.com"
    assert data["address"] == "ul. Długa 10, Wrocław"
    assert data["comment"] == None
    assert data["source"] == "web_form"



def test_ingest_merges_duplicate_by_email(client, db_session):
    first_payload = {
        "name": "Michał Kowalski",
        "age": "26",
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": "",
        "source": "web_form",
    }
    response = client.post("/ingest", json=first_payload)
    assert response.status_code == 200

    second_payload = {
        "name": "Michau Kowalski",
        "age": "26",
        "phone_number": "123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }
    response = client.post("/ingest", json=second_payload)
    assert response.status_code == 200

    # Second profile wasnt created
    assert db_session.query(Profile).count() == 1

    # Get the only profile
    profile = db_session.query(Profile).first()

    # It is still first profile
    assert profile.email == "michal@example.com"
    assert profile.first_name == "Michał"
    assert profile.last_name == "Kowalski"
    assert profile.phone_number == "+48123456789"