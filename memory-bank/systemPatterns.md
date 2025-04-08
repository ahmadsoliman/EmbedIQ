# System Patterns: EmbedIQ

## System Architecture

EmbedIQ follows a microservices architecture with containerized components to ensure scalability, maintainability, and resilience. The architecture consists of several key components:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  Frontend App   │◄────►│    API Layer    │◄────►│  Core RAG       │
│  (React)        │      │   (FastAPI)     │      │  Processing     │
│                 │      │                 │      │                 │
└─────────────────┘      └────────┬────────┘      └────────┬────────┘
                                  │                        │
                                  │                        │
                                  ▼                        ▼
                         ┌─────────────────┐      ┌─────────────────┐
                         │                 │      │                 │
                         │   PostgreSQL    │◄────►│  LightRAG       │
                         │   Database      │      │  Framework      │
                         │                 │      │                 │
                         └─────────────────┘      └─────────────────┘
```

### Component Responsibilities

1. **Frontend App (React)**

   - User interface for end users
   - Query submission and results display
   - User authentication and management
   - Dashboard and analytics visualization

2. **API Layer (FastAPI)**

   - RESTful API endpoints for developers
   - Request validation and authentication
   - Rate limiting and usage tracking
   - Error handling and logging

3. **Core RAG Processing**

   - Document ingestion and preprocessing
   - Embedding generation
   - Vector search and context retrieval
   - LLM prompt construction and response generation

4. **PostgreSQL Database**

   - Storage for document embeddings
   - User and authentication data
   - Usage statistics and logs
   - Configuration settings

5. **LightRAG Framework**
   - Vector similarity search functionality
   - LLM integration and management
   - Context optimization and ranking
   - Response quality control

## Key Technical Decisions

### 1. Microservices Architecture

**Decision**: Adopt a microservices approach with containerized components.
**Rationale**:

- Enables independent scaling of components based on load
- Allows for isolated updates and maintenance
- Improves fault isolation and system resilience
- Facilitates development across multiple teams

### 2. Docker Containerization

**Decision**: Package all components as Docker containers.
**Rationale**:

- Ensures consistency across environments
- Simplifies deployment and scaling
- Reduces "works on my machine" issues
- Enables container orchestration with Kubernetes

### 3. FastAPI for Backend

**Decision**: Use FastAPI as the API framework.
**Rationale**:

- High performance with async support
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- Python ecosystem compatibility

### 4. PostgreSQL for Storage

**Decision**: Use PostgreSQL for all data storage needs.
**Rationale**:

- Vector extension support for embeddings
- ACID compliance for critical data
- Rich query capabilities
- Mature ecosystem and tooling

### 5. React for Frontend

**Decision**: Build the user interface with React.
**Rationale**:

- Component-based architecture for reusability
- Virtual DOM for performance optimization
- Large ecosystem of libraries and tools
- Strong developer community and support

### 6. LightRAG Framework

**Decision**: Leverage LightRAG for RAG capabilities.
**Rationale**:

- Optimized for vector search and retrieval
- Well-integrated with LLM providers
- Provides graph database functionality
- Active development and support

## Design Patterns

### Data Access Patterns

- **Repository Pattern**: Abstract database operations
- **Data Transfer Objects (DTOs)**: Clean data exchange between layers
- **CQRS** (where appropriate): Separate read and write operations

### API Patterns

- **RESTful API Design**: Resource-oriented endpoints
- **API Versioning**: Ensure backward compatibility
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **Pagination**: For large result sets

### Frontend Patterns

- **Component-Based Architecture**: Reusable UI elements
- **Flux/Redux Pattern**: State management
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Graceful degradation

### Processing Patterns

- **Event-Driven Processing**: For document ingestion
- **Pipeline Pattern**: For RAG workflow
- **Caching Strategy**: For frequently accessed embeddings
- **Idempotent Operations**: For reliable API calls

## Component Relationships

### API to Core Processing

- API layer receives requests and forwards them to the appropriate core processing service
- Authentication and validation happen at the API layer
- Core processing returns structured responses to the API layer

### Core Processing to Database

- Core processing services read/write data to PostgreSQL
- Transaction management ensures data consistency
- Connection pooling optimizes database interactions

### Frontend to API

- Frontend communicates exclusively through the API layer
- JWT authentication secures communications
- API responses are formatted for direct consumption by frontend components

### LightRAG Integration

- Core processing services leverage LightRAG for vector operations
- LightRAG interacts with the database for persistent storage
- Model management is handled through LightRAG abstractions

## Deployment Strategy

- Individual services are containerized and deployed as Docker images
- Container orchestration (Kubernetes optional) manages scaling and resilience
- CI/CD pipelines automate testing and deployment
- Blue-green deployment minimizes downtime during updates
