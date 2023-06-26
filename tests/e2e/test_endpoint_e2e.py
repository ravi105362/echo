import pytest
from pytest_httpx import HTTPXMock
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app

pytestmark = pytest.mark.asyncio

client = TestClient(app)


@pytest.fixture
def mock_db(monkeypatch, db_fix):
    monkeypatch.setattr('sqlalchemy.orm.sessionmaker', mock := MagicMock())
    mock.query.all.return_value = [
        db_fix,
    ]
    return mock


async def test_app_test(httpx_mock: HTTPXMock, mock_db, caplog):
    httpx_mock.add_response(url="http://testserver/endpoints")
    response = client.get(url="/endpoints")
    assert response.status_code == 200
    assert 'HTTP Request: GET http://testserver/endpoints "HTTP/1.1 200 OK' in caplog.text  # noqa: E501
