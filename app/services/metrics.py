"""Performance metrics collection"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.feature import Feature
from app.config import settings
from app.database import follower_engine, primary_engine
from typing import Optional
import time


class MetricsService:
    """Service for collecting performance metrics"""
    
    def __init__(self):
        self.recent_query_times: list[float] = []
        self.max_recent_queries = 100
    
    def record_query_time(self, time_ms: float):
        """Record a query execution time"""
        self.recent_query_times.append(time_ms)
        if len(self.recent_query_times) > self.max_recent_queries:
            self.recent_query_times.pop(0)
    
    def get_average_latency(self) -> Optional[float]:
        """Get average query latency from recent queries"""
        if not self.recent_query_times:
            return None
        return sum(self.recent_query_times) / len(self.recent_query_times)
    
    def get_stats(self, db: Session) -> dict:
        """Get comprehensive stats"""
        # Count total features
        total_features = db.query(func.count(Feature.id)).scalar() or 0
        
        # Check database connections
        db_connections = {
            "primary": {
                "available": primary_engine is not None,
                "pool_size": primary_engine.pool.size() if primary_engine else 0
            },
            "follower": {
                "available": follower_engine is not None,
                "pool_size": follower_engine.pool.size() if follower_engine else 0
            }
        }
        
        return {
            "total_features": total_features,
            "follower_pool_enabled": settings.use_follower_pool,
            "follower_pool_available": follower_engine is not None,
            "database_connections": db_connections,
            "recent_query_latency_ms": self.get_average_latency()
        }


# Global metrics instance
metrics_service = MetricsService()


def get_metrics_service() -> MetricsService:
    """Get metrics service instance"""
    return metrics_service

