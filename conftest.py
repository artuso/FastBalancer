from dotenv import dotenv_values
from httpx import AsyncClient
import pytest
import index

config = dotenv_values(".env")

@pytest.fixture(scope="function")
def api_client():
    client = AsyncClient(base_url=f"{config['APP_URL']}:{config['APP_PORT']}")
    return client


@pytest.fixture(scope="session")
def db_client():
    return index.db




