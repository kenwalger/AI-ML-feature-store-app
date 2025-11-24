"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

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

# Serve static files (frontend) if they exist
static_dir = Path(__file__).parent.parent / "app" / "static"
if static_dir.exists() and (static_dir / "index.html").exists():
    # Mount static assets directory
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/static/assets", StaticFiles(directory=str(assets_dir)), name="static-assets")
    
    # Mount root static directory for other files
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    @app.get("/")
    async def root():
        """Serve frontend index.html"""
        return FileResponse(str(static_dir / "index.html"))
else:
    @app.get("/")
    async def root():
        """Root endpoint - API info (frontend not built yet)"""
        return {
            "message": "AI/ML Feature Store API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "note": "Frontend not built. Run 'npm run build:frontend' to build the UI."
        }


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "follower_pool_enabled": settings.use_follower_pool,
        "follower_pool_available": settings.follower_database_url is not None
    }

