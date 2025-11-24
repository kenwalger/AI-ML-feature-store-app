"""Tests for toggle endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_follower_status(client):
    """Test getting follower pool status"""
    response = client.get("/api/toggle/follower")
    assert response.status_code == 200
    data = response.json()
    assert "follower_pool_enabled" in data
    assert "message" in data


def test_toggle_follower_pool(client):
    """Test toggling follower pool"""
    # Get current status
    current = client.get("/api/toggle/follower").json()
    current_enabled = current["follower_pool_enabled"]
    
    # Toggle (may fail if follower DB not configured)
    response = client.post("/api/toggle/follower", params={"enabled": not current_enabled})
    
    # Should return 200 or 400 (if follower not configured)
    assert response.status_code in [200, 400]

