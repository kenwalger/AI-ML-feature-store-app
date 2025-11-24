"""Database connection and setup"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator, Optional
import os

from app.config import settings

# Create base class for models
Base = declarative_base()

# Primary database engine - lazy initialization to handle missing psycopg2 gracefully
primary_engine: Optional[object] = None

def _create_primary_engine():
    """Create primary database engine with error handling"""
    global primary_engine
    if primary_engine is None:
        try:
            # Ensure we're using postgresql:// URL format
            db_url = settings.database_url
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            
            primary_engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                echo=settings.environment == "development"
            )
        except Exception as e:
            print(f"Warning: Failed to create primary database engine: {e}")
            print("This may be expected if DATABASE_URL is not set or psycopg2 is not installed")
            raise
    return primary_engine

# Initialize on import if DATABASE_URL is available
if settings.database_url:
    try:
        primary_engine = _create_primary_engine()
    except Exception:
        # Will be created lazily when needed
        pass

# Follower database engine (if configured) - lazy initialization
follower_engine: Optional[object] = None

def _create_follower_engine():
    """Create follower database engine with error handling"""
    global follower_engine
    if follower_engine is None and settings.follower_database_url:
        try:
            db_url = settings.follower_database_url
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            
            follower_engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                echo=settings.environment == "development"
            )
        except Exception as e:
            print(f"Warning: Failed to create follower database engine: {e}")
            raise
    return follower_engine

# Initialize on import if FOLLOWER_DATABASE_URL is available
if settings.follower_database_url:
    try:
        follower_engine = _create_follower_engine()
    except Exception:
        # Will be created lazily when needed
        pass

# Session makers - created lazily
PrimarySessionLocal: Optional[sessionmaker] = None
FollowerSessionLocal: Optional[sessionmaker] = None

def _get_primary_session_local():
    """Get or create primary session local"""
    global PrimarySessionLocal
    if PrimarySessionLocal is None:
        engine = _create_primary_engine()
        PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return PrimarySessionLocal

def _get_follower_session_local():
    """Get or create follower session local"""
    global FollowerSessionLocal
    if FollowerSessionLocal is None and settings.follower_database_url:
        engine = _create_follower_engine()
        if engine:
            FollowerSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return FollowerSessionLocal


def init_db():
    """Initialize database and enable pgvector extension"""
    try:
        engine = _create_primary_engine()
        with engine.connect() as conn:
            # Enable pgvector extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # If follower exists, ensure it has pgvector too
        if settings.follower_database_url:
            try:
                follower = _create_follower_engine()
                if follower:
                    with follower.connect() as conn:
                        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                        conn.commit()
            except Exception as e:
                print(f"Warning: Could not initialize follower database: {e}")
    except Exception as e:
        print(f"Warning: Database initialization error (may be expected in some environments): {e}")
        raise


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
    if use_follower:
        session_local = _get_follower_session_local()
        if session_local:
            db = session_local()
        else:
            # Fall back to primary if follower not available
            db = _get_primary_session_local()()
    else:
        db = _get_primary_session_local()()
    
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context(use_follower: bool = None):
    """Context manager for database sessions"""
    if use_follower is None:
        use_follower = settings.use_follower_pool
    
    if use_follower:
        session_local = _get_follower_session_local()
        if session_local:
            db = session_local()
        else:
            # Fall back to primary if follower not available
            db = _get_primary_session_local()()
    else:
        db = _get_primary_session_local()()
    
    try:
        yield db
    finally:
        db.close()


# Allow running as module for Heroku release phase
if __name__ == "__main__":
    init_db()
