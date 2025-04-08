# Active Context: EmbedIQ

## Current Work Focus

The project is currently in the initial setup phase. We're establishing the memory bank and planning the core architecture based on the product specification document. The focus areas are:

1. **Project Documentation**: Creating a comprehensive memory bank to guide development.
2. **Architecture Planning**: Finalizing the system design and component interactions.
3. **Development Environment**: Preparing to set up the initial development environment.

## Recent Changes

- Created Memory Bank foundation documents:
  - `projectbrief.md`: Core requirements and goals
  - `productContext.md`: Why the project exists and problems it solves
  - `systemPatterns.md`: System architecture and key technical decisions
  - `techContext.md`: Technologies, development setup, constraints
  - `activeContext.md`: Current work focus (this document)
  - `progress.md`: Project progress tracking

## Active Decisions

### Currently Considering

- **UI Framework Selection**: Deciding between Material-UI and Tailwind CSS for the frontend.
- **Deployment Strategy**: Determining whether to use Kubernetes or simpler orchestration for initial deployment.
- **LLM Provider Integration**: Evaluating which LLM providers to support initially.

### Recently Decided

- Adopting a microservices architecture with containerized components
- Using FastAPI for the backend API layer
- Using PostgreSQL with vector extensions for data storage
- Using React for the frontend application
- Using LightRAG as the core RAG framework

## Next Steps

### Immediate Next Steps

1. **Repository Setup**: Create the initial repository structure following the defined pattern
2. **Development Environment**: Set up Docker Compose configuration for local development
3. **Backend API Skeleton**: Create the basic FastAPI application structure
4. **Frontend Application Skeleton**: Set up the React application structure

### Short-term Goals

1. **Database Schema**: Design and implement the initial database models and migration
2. **Core API Endpoints**: Implement the essential API endpoints (health, ingest, search, query)
3. **LightRAG Integration**: Set up the integration with the LightRAG framework
4. **Basic Frontend UI**: Create the initial UI layout and navigation

### Medium-term Goals

1. **Authentication System**: Implement user authentication and authorization
2. **Document Processing Pipeline**: Build the document ingestion and processing system
3. **Vector Search Implementation**: Implement the embedding search functionality
4. **Query Interface**: Create the user interface for submitting and viewing query results

## Current Challenges

1. **LightRAG Integration**: Need to explore the LightRAG framework capabilities and integration points
2. **Vector Database Performance**: Need to evaluate PostgreSQL performance with vector extensions
3. **LLM Provider Selection**: Need to determine the best LLM provider based on performance and cost
4. **Development Workflow**: Need to establish effective development practices for the team

## Team Context

The project is currently in the planning phase. The development team will consist of:

- Backend developers with Python/FastAPI experience
- Frontend developers with React experience
- DevOps engineers for containerization and CI/CD
- AI/ML specialists for LightRAG and LLM integration

## Important Links

- Project Documentation: Located in the memory-bank directory
- Product Specification: Original document used to create the memory bank
- Development Guidelines: To be established in the docs directory

## Communication Protocols

- GitHub Issues for task tracking
- Pull Requests with code reviews for all changes
- Documentation updates with every significant feature implementation
- Regular system architecture reviews as the project evolves
