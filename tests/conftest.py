"""
Shared test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI application.
    Each test gets a fresh client instance with a clean app state.
    """
    return TestClient(app)
