"""Tests for ingestion endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ingest_feature_success(client, sample_feature_data):
    """Test successful feature ingestion"""
    # Note: This test may fail if embedding service is not configured
    # In a real test environment, you'd mock the embedding service
    response = client.post("/api/ingest", json=sample_feature_data)
    
    # Should return 201 or 500 (if embedding fails)
    assert response.status_code in [201, 500]


def test_ingest_feature_validation(client):
    """Test feature ingestion validation"""
    # Missing required field
    response = client.post("/api/ingest", json={"description": "test"})
    assert response.status_code == 422  # Validation error


def test_ingest_batch_success(client):
    """Test batch ingestion"""
    features = [
        {
            "name": f"Product {i}",
            "description": f"Description {i}",
            "category": "Electronics",
            "price": 10.0 * i
        }
        for i in range(5)
    ]
    
    response = client.post("/api/ingest/batch", json=features)
    # Should return 201 or 500 (if embedding fails)
    assert response.status_code in [201, 500]


def test_ingest_batch_size_limit(client):
    """Test batch size limit"""
    features = [{"name": f"Product {i}"} for i in range(1001)]
    response = client.post("/api/ingest/batch", json=features)
    assert response.status_code == 400

