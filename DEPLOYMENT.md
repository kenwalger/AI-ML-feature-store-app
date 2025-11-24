# Heroku Deployment Guide

## Required Add-ons

This application requires the following Heroku add-ons:

### 1. Heroku Postgres (Primary Database)
```bash
heroku addons:create heroku-postgresql:essential-0
```
This provides the primary database with pgvector support.

### 2. Heroku Postgres Follower (Optional but Recommended for Demo)
```bash
heroku addons:create heroku-postgresql:essential-0 --follow DATABASE_URL --name DATABASE_FOLLOWER
```
This creates a follower database to demonstrate follower pool capabilities.

**Note**: After creating the follower, set the environment variable:
```bash
heroku config:set FOLLOWER_DATABASE_URL=$(heroku config:get DATABASE_FOLLOWER_URL)
```

### 3. Redis (Required for Celery)
```bash
heroku addons:create heroku-redis:mini
```
This provides Redis for Celery background job processing.

### 4. Heroku Managed Inference (Required for Embeddings)
```bash
heroku addons:create heroku-ai:basic
```
This provides access to Cohere embeddings via Heroku Managed Inference.

**Note**: After creating the addon, get your API key:
```bash
heroku config:get HEROKU_AI_API_KEY
```

## Deployment Steps

### 1. Create Heroku App
```bash
heroku create your-app-name
```

### 2. Set Buildpacks
The `.buildpacks` file will be automatically detected, or set manually:
```bash
heroku buildpacks:add https://github.com/astral-sh/uv-heroku-buildpack
heroku buildpacks:add heroku/python
```

### 3. Provision Add-ons
Run all the addon creation commands above.

### 4. Set Environment Variables
```bash
heroku config:set USE_FOLLOWER_POOL=false
heroku config:set HEROKU_AI_MODEL_ID=cohere-embed-english-v3.0

# If you created a follower database:
heroku config:set FOLLOWER_DATABASE_URL=$(heroku config:get DATABASE_FOLLOWER_URL)
```

### 5. Deploy
```bash
git push heroku main
```

### 6. Initialize Database
```bash
heroku run python -c "from app.database import init_db; init_db()"
```

### 7. Seed Sample Data (Optional)
```bash
heroku run python scripts/seed_data.py 100
```

## Troubleshooting

### Build Failures

If the build fails with uv-related errors:
1. Ensure `.buildpacks` file exists and lists the uv buildpack first
2. Check that `pyproject.toml` or `requirements.txt` exists
3. The buildpack will automatically install uv - no manual installation needed

### Database Connection Issues

If you see database connection errors:
1. Verify Postgres addon is provisioned: `heroku addons`
2. Check DATABASE_URL is set: `heroku config:get DATABASE_URL`
3. Ensure pgvector extension is enabled (handled by init_db)

### Embedding Service Issues

If embeddings fail:
1. Verify Heroku AI addon is provisioned
2. Check HEROKU_AI_API_KEY is set: `heroku config:get HEROKU_AI_API_KEY`
3. Verify the model ID is correct: `heroku config:get HEROKU_AI_MODEL_ID`

## Cost Considerations

- **Essential-0 Postgres**: Free tier available (limited connections)
- **Redis Mini**: Free tier available (25MB memory)
- **Heroku AI Basic**: Check current pricing
- **Follower Database**: Additional cost (optional for demo)

For production demos, consider:
- Using Standard tier Postgres for better performance
- Scaling dynos based on traffic
- Monitoring addon usage

