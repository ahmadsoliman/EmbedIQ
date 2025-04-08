# Technical Context: EmbedIQ

## Technologies Used

### Backend Technologies

- **Language**: Python 3.10+
- **API Framework**: FastAPI
- **ASGI Server**: Uvicorn/Gunicorn
- **ORM**: SQLAlchemy 2.0
- **Data Validation**: Pydantic v2
- **Authentication**: JWT, OAuth2
- **Documentation**: OpenAPI (Swagger), ReDoc

### Frontend Technologies

- **Framework**: React 18+
- **Build Tool**: Vite
- **State Management**: React Context API and/or Redux
- **UI Components**: Material-UI
- **API Client**: Axios or React Query
- **Testing**: Jest, React Testing Library

### Data Storage

- **Primary Database**: PostgreSQL 14+
- **Vector Extensions**: pgvector for embedding storage
- **Graph Storage**: Apache AGE for graph relationships
- **Migrations**: Alembic
- **Connection Pooling**: PgBouncer (optional for production)

### AI/LLM Technologies

- **RAG Framework**: LightRAG
- **Embedding Models**: Sentence Transformers, OpenAI Embeddings
- **LLM Providers**: OpenAI, Anthropic, or others as needed
- **Context Processing**: LangChain components (optional)

### DevOps & Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose (development), Kubernetes (optional for production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: Loguru, OpenTelemetry
- **Secret Management**: Docker Secrets or environment variables

## Development Setup

### Local Development Environment

1. **Prerequisites**:

   - Python 3.10+
   - Node.js 18+
   - Docker and Docker Compose
   - Git

2. **Repository Structure**:

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

3. **Setup Steps**:
   - Clone repository
   - Run `docker-compose up` to start all services
   - Access API at http://localhost:8000
   - Access frontend at http://localhost:3000
   - API documentation at http://localhost:8000/docs

### LightRAG Integration

1. **Component Structure**:

   - `LightRAGService` singleton class for managing LightRAG instances
   - PostgreSQL storage for vectors, knowledge graph, and key-value data
   - API endpoints for text ingestion and querying

2. **Storage Configuration**:

   - Vector storage: PostgreSQL with pgvector
   - Graph storage: PostgreSQL with Apache AGE
   - Key-value storage: PostgreSQL

3. **Environment Variables**:

   - `DATABASE_URL`: PostgreSQL connection string
   - `LIGHTRAG_WORKING_DIR`: Directory for LightRAG data
   - `AGE_GRAPH_NAME`: Name for the Apache AGE graph

4. **Query Modes**:
   - `naive`: Basic search without advanced techniques
   - `local`: Context-dependent information retrieval
   - `global`: Utilizing global knowledge graph
   - `hybrid`: Combining local and global retrieval
   - `mix`: Integrating knowledge graph and vector retrieval

### Database Migration Workflow

1. Create models in SQLAlchemy
2. Generate migration with Alembic
3. Review and adjust migration as needed
4. Apply migration to database
5. Verify schema changes

### API Development Workflow

1. Define data models with Pydantic
2. Implement business logic in services
3. Create API endpoints in routers
4. Add validation and error handling
5. Document with OpenAPI comments
6. Write tests for new functionality

### Frontend Development Workflow

1. Create/modify components
2. Update API client for new endpoints
3. Implement state management
4. Add styling and responsiveness
5. Write tests for components
6. Optimize for performance

## Technical Constraints

### Performance Requirements

- **API Response Time**: 95% of API requests should complete in <500ms
- **Search Latency**: Vector search operations should complete in <200ms
- **LLM Response Time**: End-to-end query processing should aim for <3s
- **Concurrent Users**: System should handle at least 100 concurrent users
- **Document Scale**: Support for at least 1M document chunks in the database

### Security Constraints

- **Authentication**: All API endpoints except health check must require authentication
- **Authorization**: Role-based access control for administrative functions
- **Data Protection**: PII must be properly encrypted at rest
- **API Security**: Rate limiting, CORS protection, input validation
- **Dependency Management**: Regular security audits of dependencies

### Deployment Constraints

- **Containerization**: All components must be containerized
- **Environment Config**: No hardcoded secrets or environment-specific values
- **Horizontal Scaling**: Stateless components must support horizontal scaling
- **Resource Utilization**: Specified resource limits for all containers
- **Health Monitoring**: Liveness and readiness probes for all services

### Compatibility Requirements

- **Browser Support**: Latest two versions of major browsers
- **Mobile Responsiveness**: Frontend must work on devices down to 320px width
- **API Versioning**: APIs must be versioned to ensure backward compatibility
- **Internationalization**: UI must support future internationalization
- **Architecture Support**: Support for both x86_64 and ARM64 (Apple Silicon) architectures

## Dependencies

### External Dependencies

- **LLM API Services**: OpenAI, Anthropic, or similar for LLM capabilities
- **Embedding Services**: OpenAI Embeddings API or local models
- **Authentication Providers**: Optional OAuth providers (Google, GitHub)
- **Monitoring Services**: Optional APM services integration

### Internal Dependencies

- **LightRAG**: Core framework for RAG capabilities
- **PostgreSQL**: Primary data store with vector extensions (pgvector) and graph extensions (Apache AGE)
- **Redis**: Optional for caching and rate limiting

### Known Issues

- **PostgreSQL Docker Image on ARM64**: The current PostgreSQL Docker image with pgvector and Apache AGE extensions crashes when attempting to create extensions on ARM64 architecture (Apple Silicon). We need to find or create a more compatible image.
- **SQLAlchemy Naming Conflict**: The 'metadata' attribute in SQLAlchemy models conflicts with SQLAlchemy's internal metadata usage, requiring renaming in our models.
- **LightRAG on Apple Silicon**: Need to ensure compatibility with ARM64 architecture for all components.

### Licensing Considerations

- All dependencies must have compatible licenses (MIT, Apache 2.0, etc.)
- Commercial use of LLM APIs requires appropriate enterprise licensing
- Open source components should be carefully vetted for licensing restrictions

### Versioning Strategy

- **Semantic Versioning**: All components follow semver
- **Dependency Pinning**: All dependencies have explicit versions
- **Compatibility Matrix**: Documented compatibility between component versions
- **Upgrade Path**: Clear process for upgrading dependencies

## Technical Debt & Considerations

- Regular dependency updates must be scheduled
- Test coverage metrics must be maintained above threshold
- Code quality tools must be integrated into CI pipeline
- Performance benchmarks must be established and monitored
- Documentation must be kept updated with code changes
- ARM64 architecture compatibility must be regularly tested and maintained
