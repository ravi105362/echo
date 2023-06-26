import pytest
from src.router import endpoints
from unittest.mock import ANY, MagicMock


@pytest.fixture
def response():
    return MagicMock()


@pytest.fixture
def database():
    res = MagicMock()
    res.query.all = ["abc", "def"]
    return res


@pytest.mark.asyncio
async def test_read_all_with_no_response(response, database):
    res = await endpoints.read_all(response, database)
    assert res == {'data': []}


@pytest.mark.asyncio
async def test_read_all_with_one_response(response, database, db_fix):

    database.query().all.return_value = [
        db_fix,
    ]
    res = await endpoints.read_all(response, database)
    assert res == {'data': [ANY]}


@pytest.mark.asyncio
async def test_root(response, database, db_fix):
    database.query().filter().first().body = db_fix.body
    res = await endpoints.read_root("/greet", response, database)
    assert res == "Hello Pytest"
