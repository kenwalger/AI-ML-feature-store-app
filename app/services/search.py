"""Vector search service"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Tuple
from app.models.feature import Feature
from app.models.schemas import FeatureResponse, SearchResult
from app.services.embedding import get_embedding_service
import numpy as np


class SearchService:
    """Service for vector similarity search"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    async def search_similar(
        self,
        db: Session,
        query_text: str,
        limit: int = 10,
        threshold: float = 0.0
    ) -> List[Tuple[Feature, float]]:
        """
        Search for similar features using vector similarity.
        
        Returns:
            List of (Feature, similarity_score) tuples
        """
        # Generate embedding for query
        try:
            query_embedding = await self.embedding_service.generate_embedding(query_text)
        except Exception as e:
            raise Exception(f"Failed to generate query embedding: {e}")
        
        # Convert to string format for pgvector
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Perform vector similarity search using cosine distance
        # pgvector uses 1 - cosine_similarity as distance, so we want to order by distance ASC
        # Use CAST() instead of :: to avoid SQLAlchemy parameter binding issues
        query = text("""
            SELECT id, name, description, category, price, created_at,
                   1 - (embedding <=> CAST(:embedding AS vector)) as similarity
            FROM features
            WHERE embedding IS NOT NULL
            AND (1 - (embedding <=> CAST(:embedding AS vector))) >= :threshold
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        result = db.execute(
            query,
            {
                "embedding": embedding_str,
                "threshold": threshold,
                "limit": limit
            }
        )
        
        # Fetch results and create Feature objects
        results = []
        for row in result:
            feature = Feature(
                id=row.id,
                name=row.name,
                description=row.description,
                category=row.category,
                price=row.price,
                created_at=row.created_at
            )
            similarity = float(row.similarity)
            results.append((feature, similarity))
        
        return results


def get_search_service() -> SearchService:
    """Get search service instance"""
    return SearchService()

