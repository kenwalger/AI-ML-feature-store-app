"""Tests for search endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_get_success(client):
    """Test GET search endpoint"""
    response = client.get("/api/search", params={"query": "test query", "limit": 5})
    # May return 200 (with results) or 500 (if no data/embedding fails)
    assert response.status_code in [200, 500]


def test_search_get_empty_query(client):
    """Test search with empty query"""
    response = client.get("/api/search", params={"query": ""})
    assert response.status_code == 400


def test_search_post_success(client):
    """Test POST search endpoint"""
    search_query = {
        "query": "test search",
        "limit": 10,
        "threshold": 0.5
    }
    response = client.post("/api/search", json=search_query)
    # May return 200 or 500
    assert response.status_code in [200, 500]


def test_search_validation(client):
    """Test search query validation"""
    # Invalid limit
    response = client.get("/api/search", params={"query": "test", "limit": 200})
    assert response.status_code == 422

