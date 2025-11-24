"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.routes import ingestion, search, features, stats, toggle
from app.database import init_db
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="AI/ML Feature Store - Heroku NGPG Demo",
    description="Production-ready ML feature store showcasing Heroku Next Generation PostgreSQL features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingestion.router)
app.include_router(search.router)
app.include_router(features.router)
app.include_router(stats.router)
app.include_router(toggle.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI/ML Feature Store API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "follower_pool_enabled": settings.use_follower_pool,
        "follower_pool_available": settings.follower_database_url is not None
    }

