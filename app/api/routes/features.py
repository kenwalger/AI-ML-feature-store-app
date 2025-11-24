"""Feature lookup API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_database
from app.models.schemas import FeatureResponse
from app.models.feature import Feature

router = APIRouter(prefix="/api/features", tags=["features"])


@router.get("/{feature_id}", response_model=FeatureResponse)
async def get_feature(
    feature_id: int,
    db: Session = Depends(get_database)  # Uses follower if enabled
):
    """Get a feature by ID. Reads from follower pool if enabled."""
    feature = db.query(Feature).filter(Feature.id == feature_id).first()
    
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    return FeatureResponse.model_validate(feature)

