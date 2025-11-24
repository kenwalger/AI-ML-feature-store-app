"""Database connection and setup"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import os

from app.config import settings

# Create base class for models
Base = declarative_base()

# Primary database engine
primary_engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=settings.environment == "development"
)

# Follower database engine (if configured)
follower_engine = None
if settings.follower_database_url:
    follower_engine = create_engine(
        settings.follower_database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=settings.environment == "development"
    )

# Session makers
PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
FollowerSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=follower_engine) if follower_engine else None


def init_db():
    """Initialize database and enable pgvector extension"""
    try:
        with primary_engine.connect() as conn:
            # Enable pgvector extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        
        # Create all tables
        Base.metadata.create_all(bind=primary_engine)
        
        # If follower exists, ensure it has pgvector too
        if follower_engine:
            with follower_engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
    except Exception as e:
        print(f"Warning: Database initialization error (may be expected in some environments): {e}")


def get_db(use_follower: bool = None) -> Generator[Session, None, None]:
    """
    Get database session.
    
    Args:
        use_follower: If True, use follower DB. If False, use primary.
                     If None, use settings.use_follower_pool
    """
    if use_follower is None:
        use_follower = settings.use_follower_pool
    
    # If follower requested but not available, fall back to primary
    if use_follower and FollowerSessionLocal:
        db = FollowerSessionLocal()
    else:
        db = PrimarySessionLocal()
    
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context(use_follower: bool = None):
    """Context manager for database sessions"""
    if use_follower is None:
        use_follower = settings.use_follower_pool
    
    if use_follower and FollowerSessionLocal:
        db = FollowerSessionLocal()
    else:
        db = PrimarySessionLocal()
    
    try:
        yield db
    finally:
        db.close()


# Allow running as module for Heroku release phase
if __name__ == "__main__":
    init_db()
