"""Database routing utilities for follower pool management"""
from app.config import settings
from app.database import get_db_context
from sqlalchemy.orm import Session
from typing import Callable, Any
import time


def get_active_db_type() -> str:
    """Get the currently active database type"""
    if settings.use_follower_pool and settings.follower_database_url:
        return "follower"
    return "primary"


def execute_with_timing(
    func: Callable[[Session], Any],
    use_follower: bool = None
) -> tuple[Any, float, str]:
    """
    Execute a database operation and measure its timing.
    
    Returns:
        (result, time_ms, db_type)
    """
    start_time = time.time()
    db_type = get_active_db_type() if use_follower is None else ("follower" if use_follower else "primary")
    
    with get_db_context(use_follower=use_follower) as db:
        result = func(db)
        db.commit()
    
    elapsed_ms = (time.time() - start_time) * 1000
    return result, elapsed_ms, db_type

