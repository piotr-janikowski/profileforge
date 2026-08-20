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