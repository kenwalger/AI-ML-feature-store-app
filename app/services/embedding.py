"""Cohere embedding service using Heroku Managed Inference"""
import httpx
import os
from typing import List, Optional
from app.config import settings


class EmbeddingService:
    """Service for generating embeddings using Heroku Managed Inference (Cohere)"""
    
    def __init__(self):
        self.api_key = settings.heroku_ai_api_key or os.getenv("HEROKU_AI_API_KEY")
        self.model_id = settings.heroku_ai_model_id
        self.base_url = "https://api.heroku.com"
        
        if not self.api_key:
            raise ValueError("HEROKU_AI_API_KEY must be set for embedding generation")
    
    def _get_headers(self) -> dict:
        """Get API headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.heroku+json; version=3",
            "Content-Type": "application/json"
        }
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using Heroku Managed Inference.
        
        Uses the Heroku AI API endpoint. The API key should be set via
        HEROKU_AI_API_KEY environment variable or config.
        """
        async with httpx.AsyncClient() as client:
            # Heroku Managed Inference API endpoint
            # Format: https://api.heroku.com/ai/models/{model_id}/call
            url = f"{self.base_url}/ai/models/{self.model_id}/call"
            
            payload = {
                "input": text
            }
            
            try:
                response = await client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract embedding from response
                # Response format may vary - check for common patterns
                if "embedding" in data:
                    return data["embedding"]
                elif "output" in data:
                    output = data["output"]
                    if isinstance(output, list):
                        return output
                    elif isinstance(output, dict) and "embedding" in output:
                        return output["embedding"]
                elif isinstance(data, list):
                    # Direct list response
                    return data
                else:
                    # Try to find any list field that looks like an embedding
                    for key, value in data.items():
                        if isinstance(value, list) and len(value) > 100:  # Embeddings are typically long vectors
                            return value
                    raise ValueError(f"Unexpected response format: {data}")
                    
            except httpx.HTTPError as e:
                # If API call fails, provide helpful error message
                error_detail = str(e)
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                    except:
                        error_detail = e.response.text
                raise Exception(f"Failed to generate embedding via Heroku AI API: {error_detail}")
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings


# Global instance
embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance"""
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService()
    return embedding_service

