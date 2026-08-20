from app.models.profile_model import Profile

def test_get_nonexistent_profile_returns_404(client):
    response = client.get("/profiles/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"


def test_create_profile_without_required_address_returns_422(client):
    payload = {
        "name": "Michał Kowalski",
        "age": "26",
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        #"address": "ul. Długa 10, Wrocław",
        "comment": "",
        "source": "web_form",
    }

    response = client.post("/profiles/", json=payload)

    assert response.status_code == 422


def test_create_profile(client, db_session):
    payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["first_name"] == "Michał"
    assert data["last_name"] == "Kowalski"
    assert data["email"] == "michal@example.com"

    profile = db_session.query(Profile).first()

    assert profile is not None
    assert profile.first_name == "Michał"
    assert profile.last_name == "Kowalski"
    assert profile.email == "michal@example.com"


def test_update_profile(client):
    create_payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=create_payload)

    assert response.status_code == 201

    profile_id = response.json()["id"]

    update_payload = {
        "age": 27,
        "comment": "Updated profile",
    }

    response = client.put(
        f"/profiles/{profile_id}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["age"] == 27
    assert data["comment"] == "Updated profile"
    assert data["first_name"] == "Michał"
    assert data["last_name"] == "Kowalski"


def test_update_nonexistent_profile_returns_404(client):
    update_payload = {
        "age": 27,
        "comment": "Updated profile",
    }

    response = client.put("/profiles/9999", json=update_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"


def test_delete_profile(client):
    create_payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=create_payload)

    assert response.status_code == 201

    profile_id = response.json()["id"]

    response = client.delete(f"/profiles/{profile_id}")

    assert response.status_code == 204


def test_delete_nonexistent_profile_returns_404(client):
    response = client.delete("/profiles/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"


def test_get_existing_profile(client):
    create_payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=create_payload)

    assert response.status_code == 201

    profile_id = response.json()["id"]

    response = client.get(f"/profiles/{profile_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == profile_id
    assert data["first_name"] == "Michał"
    assert data["last_name"] == "Kowalski"
    assert data["email"] == "michal@example.com"


def test_list_profiles(client):
    payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=payload)

    assert response.status_code == 201

    response = client.get("/profiles/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["first_name"] == "Michał"
    assert data[0]["last_name"] == "Kowalski"


def test_list_profiles_by_email(client):
    payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=payload)
    assert response.status_code == 201

    response = client.get("/profiles/?email=michal@example.com")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["email"] == "michal@example.com"


def test_list_profiles_by_source(client):
    payload = {
        "first_name": "Michał",
        "last_name": "Kowalski",
        "age": 26,
        "phone_number": "+48123456789",
        "email": "michal@example.com",
        "address": "ul. Długa 10, Wrocław",
        "comment": None,
        "source": "web_form",
    }

    response = client.post("/profiles/", json=payload)
    assert response.status_code == 201

    response = client.get("/profiles/?source=web_form")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["source"] == "web_form"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}