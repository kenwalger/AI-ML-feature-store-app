"""FastAPI dependencies"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db


def get_database(use_follower: bool = None) -> Session:
    """Dependency for database session"""
    return next(get_db(use_follower=use_follower))

