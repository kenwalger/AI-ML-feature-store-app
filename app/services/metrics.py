"""Performance metrics collection"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.feature import Feature
from app.config import settings
from app.database import _create_follower_engine, _create_primary_engine
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
        try:
            primary = _create_primary_engine()
            primary_available = primary is not None
            primary_pool_size = primary.pool.size() if primary else 0
        except Exception:
            primary_available = False
            primary_pool_size = 0
        
        try:
            follower = _create_follower_engine()
            follower_available = follower is not None
            follower_pool_size = follower.pool.size() if follower else 0
        except Exception:
            follower_available = False
            follower_pool_size = 0
        
        db_connections = {
            "primary": {
                "available": primary_available,
                "pool_size": primary_pool_size
            },
            "follower": {
                "available": follower_available,
                "pool_size": follower_pool_size
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

