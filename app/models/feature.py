"""Feature database model with pgvector support"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Index
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base


class Feature(Base):
    """Feature model with vector embedding"""
    __tablename__ = "features"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    price = Column(Float, nullable=True)
    
    # Vector embedding (1536 dimensions for Cohere embed-english-v3.0)
    embedding = Column(Vector(1024), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Index for vector similarity search
    __table_args__ = (
        Index('idx_embedding', 'embedding', postgresql_using='ivfflat', postgresql_with={'lists': 100}),
    )
    
    def __repr__(self):
        return f"<Feature(id={self.id}, name='{self.name}', category='{self.category}')>"

