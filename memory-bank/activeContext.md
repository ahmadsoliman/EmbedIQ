# Active Context: EmbedIQ

## Current Work Focus

The project is now in the initial implementation phase after completing the setup and scaffolding. We've established the basic structure and components for both backend and frontend. We are currently implementing RAG functionality with LightRAG.

1. **Project Structure**: Created the initial repository structure following the defined patterns.
2. **Backend API**: Implemented the basic FastAPI application with core endpoints.
3. **Frontend Structure**: Set up the React application with essential pages and components.
4. **Development Environment**: Configured Docker and Docker Compose for local development.
5. **LightRAG Integration**: Implementing LightRAG as the RAG framework with PostgreSQL storage.

## Recent Changes

- Created complete project structure including:
  - API backend with FastAPI
  - React frontend with Material-UI
  - PostgreSQL database with pgvector
  - Docker and Docker Compose configuration
- Implemented API components:
  - Core FastAPI application structure
  - Data models and schemas
  - API endpoints for ingestion, search, and queries
  - Service layer for business logic
- Implemented Frontend components:
  - React application with routing
  - Layout with header and footer
  - Home, Query, Docs, and NotFound pages
  - Material-UI theming
- Implemented LightRAG integration:
  - Created LightRAGService with retry logic
  - Added endpoints for text ingestion and RAG queries
  - Fixed SQLAlchemy naming conflicts with metadata
  - Added database initialization scripts

## Active Decisions

### Currently Considering

- **UI Refinement**: Further refinements to the frontend UI based on user feedback.
- **API Extensions**: Additional API functionality beyond the core endpoints.
- **Testing Strategy**: Comprehensive testing approach for both backend and frontend.
- **CI/CD Pipeline**: Setting up automated testing and deployment.
- **PostgreSQL Image Selection**: Finding a PostgreSQL image with pgvector and Apache AGE that works well on ARM64 architecture (Apple Silicon).

### Recently Decided

- Used Material-UI for the frontend UI framework
- Implemented a containerized approach with Docker Compose
- Structured the backend with clear separation of concerns (routers, services, models)
- Used pgvector for PostgreSQL vector support
- Selected LightRAG as our RAG framework for its flexibility and integration with PostgreSQL

## Next Steps

### Immediate Next Steps

1. **Database Image Compatibility**: Replace the current PostgreSQL Docker image with one that works properly on ARM64 architecture (Apple Silicon Macs)
2. **Complete LightRAG Integration**: Finish debugging and testing LightRAG with PostgreSQL
3. **Authentication**: Implement authentication and authorization
4. **Document Processing**: Implement the complete document processing pipeline
5. **Frontend API Integration**: Connect the frontend to the backend API

### Short-term Goals

1. **Vector Search Implementation**: Complete the embedding generation and vector search
2. **LLM Integration**: Implement the actual LLM integration (vs. current mock)
3. **Test Coverage**: Add unit and integration tests
4. **API Documentation**: Complete the OpenAPI documentation

### Medium-term Goals

1. **Performance Optimization**: Optimize performance for both API and frontend
2. **Monitoring**: Implement monitoring and logging
3. **User Management**: Add user management functionality
4. **Advanced Search Features**: Implement filters, facets, and other search enhancements

## Current Challenges

1. **PostgreSQL + pgvector on ARM64**: We're experiencing Docker image compatibility issues with the PostgreSQL image that includes pgvector and Apache AGE extensions on Apple Silicon (ARM64) architecture. The current image is causing PostgreSQL to crash when creating extensions.
2. **LLM Integration**: Need to finalize the approach for LLM integration
3. **Vector Database Performance**: Need to evaluate PostgreSQL with pgvector in real-world scenarios
4. **Frontend-Backend Communication**: Ensuring smooth communication between frontend and API
5. **Docker Compose Development**: Optimizing the development experience with Docker Compose

## Team Context

The development plan includes:

- Backend developers focusing on FastAPI, PostgreSQL, and vector search
- Frontend developers working on React components and API integration
- DevOps setting up the containerization and CI/CD
- AI/ML specialists for embedding generation and LLM integration

## Important Links

- Project Documentation: Located in the memory-bank directory
- API Endpoints: Defined in the API routers
- Frontend Routes: Defined in the App.jsx component
- LightRAG Documentation: https://github.com/HKUDS/LightRAG

## Communication Protocols

- GitHub Issues for task tracking
- Pull Requests with code reviews for all changes
- Documentation updates with every significant feature implementation
- Regular architecture reviews as the project evolves
