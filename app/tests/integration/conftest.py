import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.profile_model import Profile

load_dotenv()

TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_TEST_USER')}:"
    f"{os.getenv('POSTGRES_TEST_PASSWORD')}@localhost:5433/"
    f"{os.getenv('POSTGRES_TEST_DB')}"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")   # scope="function" mówi: "uruchom to od nowa dla każdego pojedynczego testu", nie raz na cały plik czy całą sesję testów.
                                    # To gwarantuje, że każdy test dostaje czystą bazę, bez śladów po poprzednim teście.
def db_session():                   # to jest "setup/teardown" - przed yield tworzy wszystkie tabele od zera (create_all)
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session   # po yield (czyli po zakończeniu testu, niezależnie czy przeszedł czy nie) zamyka sesję 
    finally:            # i kasuje wszystkie tabele (drop_all) — żeby następny test znów zaczynał od zera.
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():      # Sedno mechanizmu dependency override
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db  # Wszędzie, gdzie w kodzie jest Depends(get_db), na czas tego testu podstaw zamiast tego override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()    # sprzątanie tej podmiany po teście, żeby kolejne testy nie zostały przypadkiem z tą podmianą na stałe.