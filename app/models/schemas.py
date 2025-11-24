"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class FeatureCreate(BaseModel):
    """Schema for creating a feature"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, ge=0)


class FeatureResponse(BaseModel):
    """Schema for feature response"""
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    """Schema for search query"""
    query: str = Field(..., min_length=1)
    limit: int = Field(10, ge=1, le=100)
    threshold: float = Field(0.0, ge=0.0, le=1.0)


class SearchResult(BaseModel):
    """Schema for individual search result"""
    feature: FeatureResponse
    similarity_score: float = Field(..., ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Schema for search response"""
    results: List[SearchResult]
    query: str
    limit: int
    database_used: str  # "primary" or "follower"
    query_time_ms: float


class StatsResponse(BaseModel):
    """Schema for stats response"""
    total_features: int
    follower_pool_enabled: bool
    follower_pool_available: bool
    database_connections: dict
    recent_query_latency_ms: Optional[float] = None


class ToggleResponse(BaseModel):
    """Schema for toggle response"""
    follower_pool_enabled: bool
    message: str

