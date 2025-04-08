# EmbedIQ

A cloud-based RAG (Retrieval Augmented Generation) system that leverages high-quality embedding search and LLM context-based answers.

## Overview

EmbedIQ provides a powerful solution for both developers and end users:

- **For Developers**: API endpoints to integrate RAG capabilities into applications
- **For End Users**: A web interface to query documents and get AI-enhanced responses

Built on a modern tech stack including Python FastAPI, React, PostgreSQL, Docker, and the LightRAG framework.

## Features

- Document ingestion and embedding generation
- High-performance vector search for relevant context retrieval
- LLM-powered context-aware responses
- Developer-friendly API with comprehensive documentation
- Intuitive web interface for end users
- Containerized microservices architecture for scalability

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- Git

### Development Setup

1. Clone the repository

   ```
   git clone <repository-url>
   cd embediq
   ```

2. Start the services with Docker Compose

   ```
   docker-compose up
   ```

3. Access the applications
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:3000

## Project Structure

```
/embediq
├── /api              # FastAPI backend
│   ├── /app
│   │   ├── /core     # Core functionality
│   │   ├── /models   # Data models
│   │   ├── /routers  # API endpoints
│   │   └── /services # Business logic
│   ├── /tests        # Backend tests
│   └── Dockerfile    # API container definition
│
├── /frontend         # React frontend
│   ├── /public       # Static assets
│   ├── /src          # Source code
│   │   ├── /components
│   │   ├── /pages
│   │   ├── /services
│   │   └── /utils
│   ├── /tests        # Frontend tests
│   └── Dockerfile    # Frontend container definition
│
├── /docs             # Documentation
├── /scripts          # Utility scripts
├── docker-compose.yml # Development configuration
└── README.md         # Project overview
```

## API Endpoints

- `POST /ingest`: Upload documents for embedding generation
- `GET/POST /search`: Perform embedding search based on query text
- `POST /query`: Submit a natural language query and get context-based answer
- `GET /health`: Health check for the API service

## Technologies Used

- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, Vite, Material-UI/Tailwind CSS
- **Database**: PostgreSQL with vector extensions
- **AI/LLM**: LightRAG, OpenAI/Anthropic integration
- **DevOps**: Docker, Docker Compose, GitHub Actions

## License

[License information]
