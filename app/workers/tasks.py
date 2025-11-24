"""Celery background tasks"""
from app.workers.celery_app import celery_app
from app.database import get_db_context
from app.services.ingestion import get_ingestion_service
from app.models.schemas import FeatureCreate
from typing import List


@celery_app.task(name="ingest_features_batch")
def ingest_features_batch_task(features_data: List[dict]):
    """
    Background task to ingest features in batch.
    
    Args:
        features_data: List of feature dictionaries
    """
    # Convert dicts to FeatureCreate objects
    features = [FeatureCreate(**f) for f in features_data]
    
    ingestion_service = get_ingestion_service()
    
    # Use primary database for writes
    with get_db_context(use_follower=False) as db:
        # Note: This is a sync function, so we need to handle async differently
        # For now, we'll use a workaround or make the service sync-compatible
        # In production, you might want to use asyncio.run() or make services sync
        import asyncio
        
        async def async_ingest():
            return await ingestion_service.ingest_features_batch(db, features)
        
        results = asyncio.run(async_ingest())
        return [{"id": f.id, "name": f.name} for f in results]


@celery_app.task(name="generate_embeddings_batch")
def generate_embeddings_batch_task(texts: List[str]):
    """
    Background task to generate embeddings for multiple texts.
    
    Args:
        texts: List of text strings to embed
    """
    from app.services.embedding import get_embedding_service
    import asyncio
    
    embedding_service = get_embedding_service()
    
    async def async_generate():
        return await embedding_service.generate_embeddings_batch(texts)
    
    return asyncio.run(async_generate())

