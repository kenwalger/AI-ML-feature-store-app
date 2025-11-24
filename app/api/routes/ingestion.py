"""Feature ingestion API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_database
from app.models.schemas import FeatureCreate, FeatureResponse
from app.services.ingestion import get_ingestion_service
import time

router = APIRouter(prefix="/api/ingest", tags=["ingestion"])


@router.post("", response_model=FeatureResponse, status_code=201)
async def ingest_feature(
    feature: FeatureCreate,
    db: Session = Depends(lambda: get_database(use_follower=False))  # Always use primary for writes
):
    """
    Ingest a single feature into the feature store.
    
    Writes always go to the primary database.
    """
    ingestion_service = get_ingestion_service()
    
    try:
        feature_record = await ingestion_service.ingest_feature(db, feature)
        return FeatureResponse.model_validate(feature_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest feature: {str(e)}")


@router.post("/batch", response_model=List[FeatureResponse], status_code=201)
async def ingest_features_batch(
    features: List[FeatureCreate],
    db: Session = Depends(lambda: get_database(use_follower=False))  # Always use primary for writes
):
    """
    Ingest multiple features in a batch.
    
    Writes always go to the primary database.
    """
    if len(features) > 1000:
        raise HTTPException(status_code=400, detail="Batch size cannot exceed 1000 features")
    
    ingestion_service = get_ingestion_service()
    
    try:
        start_time = time.time()
        feature_records = await ingestion_service.ingest_features_batch(db, features)
        elapsed_time = time.time() - start_time
        
        return [
            FeatureResponse.model_validate(f) for f in feature_records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest features: {str(e)}")

