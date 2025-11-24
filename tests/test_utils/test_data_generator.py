"""Tests for data generator utility"""
import pytest
from app.utils.data_generator import generate_feature, generate_features


def test_generate_feature():
    """Test generating a single feature"""
    feature = generate_feature()
    assert feature.name is not None
    assert len(feature.name) > 0
    assert feature.category is not None


def test_generate_feature_with_category():
    """Test generating feature with specific category"""
    feature = generate_feature(category="Electronics")
    assert feature.category == "Electronics"


def test_generate_features():
    """Test generating multiple features"""
    count = 10
    features = generate_features(count)
    assert len(features) == count
    assert all(f.name for f in features)


def test_feature_price_range():
    """Test that generated prices are reasonable"""
    feature = generate_feature(category="Electronics")
    # Electronics should have prices in reasonable range
    assert feature.price is None or feature.price >= 0

