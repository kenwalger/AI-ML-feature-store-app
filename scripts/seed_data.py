"""Script to seed the database with mock data"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, get_db_context
from app.utils.data_generator import generate_features
from app.services.ingestion import get_ingestion_service


async def seed_database(count: int = 100):
    """Seed database with mock features"""
    print(f"Initializing database...")
    init_db()
    
    print(f"Generating {count} mock features...")
    features_data = generate_features(count)
    
    print("Ingesting features into database...")
    ingestion_service = get_ingestion_service()
    
    with get_db_context(use_follower=False) as db:
        # Process in batches of 10 to avoid overwhelming the API
        batch_size = 10
        total_ingested = 0
        
        for i in range(0, len(features_data), batch_size):
            batch = features_data[i:i + batch_size]
            try:
                results = await ingestion_service.ingest_features_batch(db, batch)
                total_ingested += len(results)
                print(f"Ingested {total_ingested}/{count} features...")
            except Exception as e:
                print(f"Error ingesting batch: {e}")
                # Continue with next batch
                continue
    
    print(f"Successfully seeded {total_ingested} features!")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    asyncio.run(seed_database(count))

