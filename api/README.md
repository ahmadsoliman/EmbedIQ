# EmbedIQ API

This directory contains the backend API for the EmbedIQ RAG system built with FastAPI.

## Features

- Document ingestion and processing
- Vector embeddings and search
- LLM-powered context-aware responses
- RESTful API endpoints

## Directory Structure

```
/api
├── alembic/             # Database migration scripts
│   ├── versions/        # Generated migrations
│   ├── env.py           # Alembic environment configuration
│   └── script.py.mako   # Migration template
├── app/                 # Application code
│   ├── core/            # Core functionality
│   ├── models/          # Data models
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # FastAPI application
├── tests/               # Test files
├── Dockerfile           # Container definition
├── alembic.ini          # Alembic configuration
└── requirements.txt     # Python dependencies
```

## Getting Started

### Running Locally

1. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn app.main:app --reload
```

### Database Migrations

To create a new migration:

```bash
alembic revision --autogenerate -m "Description of change"
```

To apply migrations:

```bash
alembic upgrade head
```

## API Endpoints

- `POST /api/v1/ingest`: Upload documents for embedding generation
- `GET/POST /api/v1/search`: Search for documents by semantic similarity
- `POST /api/v1/query`: Submit a query for context-aware LLM answers
- `GET /health`: Health check

## Development

### Adding New Models

1. Define your model in `app/models/`
2. Import the model in `app/models/__init__.py`
3. Create a schema in `app/schemas/`
4. Create a migration using Alembic

### Adding New Endpoints

1. Create or modify router files in `app/routers/`
2. Implement business logic in `app/services/`
3. Include the router in `app/main.py`

## Testing

Run tests with pytest:

```bash
pytest
```
