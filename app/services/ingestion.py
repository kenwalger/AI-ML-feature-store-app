"""Feature ingestion service"""
from sqlalchemy.orm import Session
from typing import List
from app.models.feature import Feature
from app.models.schemas import FeatureCreate
from app.services.embedding import get_embedding_service
import asyncio


class IngestionService:
    """Service for ingesting features into the database"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    async def ingest_feature(self, db: Session, feature_data: FeatureCreate) -> Feature:
        """Ingest a single feature with embedding generation"""
        # Generate embedding from name and description
        text_to_embed = f"{feature_data.name}. {feature_data.description or ''}"
        
        try:
            embedding = await self.embedding_service.generate_embedding(text_to_embed)
        except Exception as e:
            # If embedding fails, create feature without embedding
            # In production, you might want to handle this differently
            print(f"Warning: Failed to generate embedding: {e}")
            embedding = None
        
        # Create feature record
        feature = Feature(
            name=feature_data.name,
            description=feature_data.description,
            category=feature_data.category,
            price=feature_data.price,
            embedding=embedding
        )
        
        db.add(feature)
        db.commit()
        db.refresh(feature)
        
        return feature
    
    async def ingest_features_batch(
        self,
        db: Session,
        features_data: List[FeatureCreate]
    ) -> List[Feature]:
        """Ingest multiple features in batch"""
        features = []
        
        # Generate embeddings for all features
        texts_to_embed = [
            f"{f.name}. {f.description or ''}" for f in features_data
        ]
        
        try:
            embeddings = await self.embedding_service.generate_embeddings_batch(texts_to_embed)
        except Exception as e:
            print(f"Warning: Failed to generate embeddings: {e}")
            embeddings = [None] * len(features_data)
        
        # Create feature records
        for feature_data, embedding in zip(features_data, embeddings):
            feature = Feature(
                name=feature_data.name,
                description=feature_data.description,
                category=feature_data.category,
                price=feature_data.price,
                embedding=embedding
            )
            db.add(feature)
            features.append(feature)
        
        db.commit()
        
        # Refresh all features
        for feature in features:
            db.refresh(feature)
        
        return features


def get_ingestion_service() -> IngestionService:
    """Get ingestion service instance"""
    return IngestionService()

