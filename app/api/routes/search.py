"""Vector search API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_database
from app.models.schemas import SearchQuery, SearchResponse, SearchResult, FeatureResponse
from app.services.search import get_search_service
from app.utils.db_router import get_active_db_type
from app.services.metrics import get_metrics_service
import time

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=SearchResponse)
async def search_features(
    query: str,
    limit: int = 10,
    threshold: float = 0.0,
    db: Session = Depends(get_database)  # Uses follower if enabled
):
    """
    Search for similar features using vector similarity search.
    
    Reads from follower pool if enabled, otherwise from primary.
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    search_service = get_search_service()
    metrics_service = get_metrics_service()
    
    try:
        start_time = time.time()
        results = await search_service.search_similar(db, query, limit, threshold)
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Record query time for metrics
        metrics_service.record_query_time(elapsed_ms)
        
        # Convert to response format
        search_results = [
            SearchResult(
                feature=FeatureResponse.model_validate(feature),
                similarity_score=score
            )
            for feature, score in results
        ]
        
        db_type = get_active_db_type()
        
        return SearchResponse(
            results=search_results,
            query=query,
            limit=limit,
            database_used=db_type,
            query_time_ms=round(elapsed_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("", response_model=SearchResponse)
async def search_features_post(
    search_query: SearchQuery,
    db: Session = Depends(get_database)  # Uses follower if enabled
):
    """
    Search for similar features using vector similarity search (POST method).
    
    Reads from follower pool if enabled, otherwise from primary.
    """
    search_service = get_search_service()
    metrics_service = get_metrics_service()
    
    try:
        start_time = time.time()
        results = await search_service.search_similar(
            db,
            search_query.query,
            search_query.limit,
            search_query.threshold
        )
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Record query time for metrics
        metrics_service.record_query_time(elapsed_ms)
        
        # Convert to response format
        search_results = [
            SearchResult(
                feature=FeatureResponse.model_validate(feature),
                similarity_score=score
            )
            for feature, score in results
        ]
        
        db_type = get_active_db_type()
        
        return SearchResponse(
            results=search_results,
            query=search_query.query,
            limit=search_query.limit,
            database_used=db_type,
            query_time_ms=round(elapsed_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

