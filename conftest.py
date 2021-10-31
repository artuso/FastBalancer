from dotenv import dotenv_values
from httpx import AsyncClient
from config.db import DB
import pytest

config = dotenv_values(".env")


@pytest.fixture(scope="function")
def api_client():
    client = AsyncClient(base_url=f"{config['APP_URL']}:{config['APP_PORT']}")
    return client


@pytest.fixture(scope="session")
def db_client():
    db = DB()
    db.clear_stand_document()
    db.add_defaults_stands('test_stands.json')
    return db


