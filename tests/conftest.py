import pytest
from src.utils import ResponseModel


@pytest.fixture
def db_fix():
    return ResponseModel(1234, "GET", "/hello", 404, {}, "Hello Pytest")
