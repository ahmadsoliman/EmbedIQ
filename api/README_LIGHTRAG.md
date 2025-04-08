# LightRAG Integration

This project integrates LightRAG, a framework for Retrieval-Augmented Generation (RAG), with a PostgreSQL database for production-level storage. This README provides instructions on setting up and using the LightRAG integration.

## Setup Instructions

### 1. Start the PostgreSQL Database

The project uses a specialized PostgreSQL Docker image with pgvector and Apache AGE extensions for RAG:

```bash
docker-compose up -d db
```

### 2. Initialize the Database

Run the database initialization script to create the necessary extensions and graph:

```bash
# From the project root
python scripts/init_lightrag_db.py
```

### 3. Create Database Indices

After initializing the database, create indices for better performance:

```bash
# Using Docker
docker exec -it rag-sass_db_1 psql -U postgres -d embediq -f /app/data/create_indices.sql

# Or using local psql client
psql -h localhost -p 5432 -U postgres -d embediq -f api/app/data/create_indices.sql
```

### 4. Start the API

Start the API service:

```bash
docker-compose up -d api
```

## Testing LightRAG

You can test the LightRAG integration using the provided test script:

```bash
# From the project root
python scripts/test_lightrag.py
```

## API Endpoints

The LightRAG integration adds the following endpoints to the API:

### Ingest Text

```http
POST /ingest/text
Content-Type: multipart/form-data

text=Your text content here
metadata={"title": "Document Title", "source": "Source", "author": "Author"}
```

### Query LightRAG

```http
POST /query/lightrag
Content-Type: application/json

{
  "query": "Your question here",
  "mode": "global",
  "top_k": 60,
  "only_context": false
}
```

Available modes:

- `local`: Focuses on context-dependent information
- `global`: Utilizes global knowledge
- `hybrid`: Combines local and global retrieval methods
- `naive`: Performs a basic search without advanced techniques
- `mix`: Integrates knowledge graph and vector retrieval

## LightRAG Configuration

LightRAG configuration options can be set in the `.env` file:

```
# LightRAG Configuration
LIGHTRAG_WORKING_DIR=./api/app/data
AGE_GRAPH_NAME=embediq
TOP_K=60
```

## Implementation Details

The LightRAG integration consists of:

1. **LightRAG Service**: A service class that initializes and manages LightRAG instances
2. **API Endpoints**: Extensions to the existing API for ingestion and querying
3. **PostgreSQL Storage**: Configurations for using PostgreSQL with pgvector and Apache AGE

## Troubleshooting

Common issues and solutions:

1. **Connection Errors**: Ensure the PostgreSQL container is running and accessible
2. **Permission Issues**: Verify database user permissions for creating extensions
3. **Missing Extensions**: Check if pgvector and Apache AGE extensions are installed correctly
4. **Apache AGE Empty Properties**: This is a known issue with Apache AGE release versions - you might need to compile from source to fix it

## Further Documentation

For more information on LightRAG, refer to:

- [LightRAG GitHub Repository](https://github.com/HKUDS/LightRAG)
- The `lightrag_service.py` file for implementation details
