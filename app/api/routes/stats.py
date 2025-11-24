"""Stats and metrics API routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_database
from app.models.schemas import StatsResponse
from app.services.metrics import get_metrics_service

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_database)):
    """Get application statistics and metrics"""
    metrics_service = get_metrics_service()
    stats = metrics_service.get_stats(db)
    
    return StatsResponse(**stats)

