import pytest
from app.tests.api_client import AppTestClient
from mixer.backend.django import mixer as _mixer


@pytest.fixture
def api() -> AppTestClient:
    return AppTestClient()


@pytest.fixture
def mixer():
    return _mixer
