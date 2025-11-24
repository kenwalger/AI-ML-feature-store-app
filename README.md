# AI/ML Feature Store - Heroku Next Generation PostgreSQL Demo

A production-ready ML feature store application showcasing Heroku's Next Generation PostgreSQL (NGPG) features, including pgvector for vector similarity search, follower pools, compute/storage decoupling, and high availability.

## Features

- **Vector Similarity Search**: Uses pgvector extension for semantic search
- **Follower Pool Toggle**: Demonstrate performance differences between primary and follower databases
- **High-Volume Ingestion**: Batch ingestion of features with async processing
- **Real-time Metrics**: Performance monitoring with Chart.js visualizations
- **Heroku Managed Inference**: Integration with Cohere embeddings via Heroku AI

## Architecture

### Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: Heroku Postgres Advanced with pgvector
- **Queue**: Celery + Redis
- **Frontend**: Vue.js 3 + Bootstrap 5
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (fast Python package installer)
- **ML/AI**: Heroku Managed Inference (Cohere Embeddings)

### NGPG Features Demonstrated

1. **Compute/Storage Decoupling**: Scale storage independently from compute
2. **Follower Pools**: Read replicas for improved query performance
3. **High Availability**: HA standby for production reliability
4. **pgvector Integration**: Vector similarity search at scale

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL 15+ with pgvector extension
- Redis (for Celery)
- Node.js 18+ (for frontend development)

## Local Development Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
git clone <repository-url>
cd "AI-ML Feature Store App"
```

### 3. Install Python Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `uv` with requirements.txt:
```bash
uv pip install -r requirements.txt
```

Or using traditional pip (if uv is not available):
```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/featurestore
FOLLOWER_DATABASE_URL=postgresql://user:password@localhost:5432/featurestore_follower
HEROKU_AI_API_KEY=your_heroku_ai_api_key
REDIS_URL=redis://localhost:6379/0
USE_FOLLOWER_POOL=false
```

### 6. Initialize Database

```bash
python -c "from app.database import init_db; init_db()"
```

### 7. Seed Sample Data (Optional)

```bash
python scripts/seed_data.py 100
```

### 8. Run Development Server

**Backend:**
```bash
uvicorn app.main:app --reload --port 5000
```

**Frontend (in separate terminal):**
```bash
cd frontend
npm run dev
```

**Celery Worker (in separate terminal):**
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

## Heroku Deployment

### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or visit https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Create Heroku App

```bash
heroku create your-app-name
```

### 3. Add Buildpacks

The project uses `.buildpacks` file which will be automatically detected. To manually set buildpacks:

```bash
heroku buildpacks:add https://github.com/astral-sh/uv-heroku-buildpack
heroku buildpacks:add heroku/python
```

**Note**: The `uv-heroku-buildpack` will automatically detect `pyproject.toml` or `requirements.txt` and use `uv` for fast dependency installation during the build process.

### 4. Provision Add-ons

**Required Add-ons:**

```bash
# Postgres (Primary) - REQUIRED
heroku addons:create heroku-postgresql:essential-0

# Redis - REQUIRED (for Celery)
heroku addons:create heroku-redis:mini

# Heroku Managed Inference - REQUIRED (for Cohere embeddings)
heroku addons:create heroku-ai:basic
```

**Optional Add-ons (Recommended for NGPG Demo):**

```bash
# Postgres Follower - OPTIONAL but recommended to showcase follower pools
heroku addons:create heroku-postgresql:essential-0 --follow DATABASE_URL --name DATABASE_FOLLOWER

# After creating follower, set the environment variable:
heroku config:set FOLLOWER_DATABASE_URL=$(heroku config:get DATABASE_FOLLOWER_URL)
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed addon setup instructions.

### 5. Set Environment Variables

```bash
heroku config:set USE_FOLLOWER_POOL=false
heroku config:set HEROKU_AI_MODEL_ID=cohere-embed-english-v3.0
```

### 6. Deploy

```bash
git push heroku main
```

The build process will:
1. Use the `uv-heroku-buildpack` to automatically install `uv`
2. Detect `pyproject.toml` or `requirements.txt`
3. Use `uv` to install dependencies (much faster than pip)
4. Build the application

**Note**: The buildpack handles `uv` installation automatically - no manual setup needed!

### 7. Run Database Migrations

```bash
heroku run python -m app.database
```

Or:
```bash
heroku run python -c "from app.database import init_db; init_db()"
```

### 8. Seed Data (Optional)

```bash
heroku run python scripts/seed_data.py 100
```

## Project Structure

```
.
├── app/                    # FastAPI application
│   ├── api/               # API routes
│   ├── models/            # Database models and schemas
│   ├── services/          # Business logic
│   ├── workers/           # Celery tasks
│   ├── utils/             # Utilities
│   └── main.py            # FastAPI app entry point
├── frontend/              # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Vue components
│   │   └── services/      # API client
│   └── package.json
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies (for compatibility)
├── pyproject.toml         # uv project configuration
├── Procfile              # Heroku process definitions
├── .buildpacks           # Heroku buildpack configuration
└── README.md
```

## API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### Key Endpoints

- `POST /api/ingest` - Ingest a single feature
- `POST /api/ingest/batch` - Ingest multiple features
- `GET /api/search?query=...` - Vector similarity search
- `GET /api/stats` - Application statistics
- `POST /api/toggle/follower` - Toggle follower pool

## Testing

Run the test suite:

```bash
pytest tests/ -v --cov=app
```

## Demo Flow

1. **Ingest Features**: Use the ingestion panel to add features to the store
2. **Toggle Follower Pool**: Switch between primary and follower database
3. **Search**: Perform vector similarity searches and observe performance
4. **Monitor**: View real-time metrics and query latency comparisons

## NGPG Features Showcase

### Follower Pool Toggle

The application includes a toggle to switch between primary and follower databases for read queries. This demonstrates:

- Reduced load on primary database
- Improved query performance for read-heavy workloads
- Real-time latency comparison

### Vector Search Performance

pgvector enables fast similarity search on embeddings:

- Semantic search across feature descriptions
- Configurable similarity thresholds
- Efficient KNN queries using IVFFlat indexing

### High Availability

- Primary database with HA standby
- Automatic failover capabilities
- Zero-downtime deployments

## Using uv Package Manager

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management. 

### Local Development

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade
```

### Heroku Deployment

The project is configured to use `uv` on Heroku via the `uv-heroku-buildpack`. The buildpack will:

1. Automatically install `uv` during the build
2. Detect `pyproject.toml` or `requirements.txt`
3. Use `uv` to install dependencies (significantly faster than pip)
4. Cache dependencies for faster subsequent builds

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](LICENSE) for details.

## Resources

- [Heroku Next Generation PostgreSQL](https://www.heroku.com/blog/introducing-the-next-generation-of-heroku-postgres)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [uv Documentation](https://github.com/astral-sh/uv)

