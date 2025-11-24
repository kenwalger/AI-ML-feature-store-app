"""Cohere embedding service using Heroku Managed Inference"""
import httpx
import os
from typing import List, Optional
from app.config import settings


class EmbeddingService:
    """Service for generating embeddings using Heroku Managed Inference (Cohere)"""
    
    def __init__(self):
        self.api_key = settings.heroku_ai_api_key or os.getenv("INFERENCE_KEY") or os.getenv("HEROKU_AI_API_KEY")
        self.model_id = settings.heroku_ai_model_id
        # Use Inference URL if available, otherwise fall back to Heroku AI API
        self.base_url = settings.inference_url or os.getenv("INFERENCE_URL") or "https://api.heroku.com"
        
        if not self.api_key:
            raise ValueError("INFERENCE_KEY or HEROKU_AI_API_KEY must be set for embedding generation")
    
    def _get_headers(self) -> dict:
        """Get API headers"""
        # New Inference API uses different header format
        if "inference.heroku.com" in self.base_url:
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            # Legacy Heroku AI API format
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/vnd.heroku+json; version=3",
                "Content-Type": "application/json"
            }
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using Heroku Managed Inference.
        
        Supports both the new Inference API and legacy Heroku AI API.
        """
        async with httpx.AsyncClient() as client:
            # Check if using new Inference API format
            if "inference.heroku.com" in self.base_url:
                # New Inference API format (Cohere accepts string or array)
                url = f"{self.base_url}/v1/embeddings"
                # Cohere models can accept string or array, but array is more standard
                payload = {
                    "model": self.model_id,
                    "input": [text] if isinstance(text, str) else text
                }
            else:
                # Legacy Heroku AI API format
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
                # New Inference API format: {"data": [{"embedding": [...]}]}
                if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                    if "embedding" in data["data"][0]:
                        return data["data"][0]["embedding"]
                
                # Legacy Heroku AI API format
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

