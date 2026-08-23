from app.services import profile_service


def test_global_exception_handler(client, monkeypatch):
    def mock_get_profile(*args, **kwargs):
        raise TestException("Something went wrong")

    monkeypatch.setattr(
        profile_service,
        "get_profile",
        mock_get_profile,
    )

    response = client.get("/profiles/1")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


class TestException(Exception):
    pass
