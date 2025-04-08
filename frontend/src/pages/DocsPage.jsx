import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Divider,
  Paper,
  Tabs,
  Tab,
} from '@mui/material';
import { useState } from 'react';

/**
 * Documentation page for the API
 */
function DocsPage() {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  return (
    <Container maxWidth='lg'>
      <Box sx={{ mb: 4 }}>
        <Typography variant='h4' component='h1' gutterBottom>
          API Documentation
        </Typography>
        <Typography color='text.secondary' paragraph>
          Integrate EmbedIQ's RAG capabilities into your applications with our
          comprehensive API.
        </Typography>

        <Paper sx={{ mt: 4 }}>
          <Tabs
            value={selectedTab}
            onChange={handleTabChange}
            indicatorColor='primary'
            textColor='primary'
            variant='fullWidth'
          >
            <Tab label='Overview' />
            <Tab label='Ingest' />
            <Tab label='Search' />
            <Tab label='Query' />
          </Tabs>
        </Paper>

        {/* Tab content */}
        <Box sx={{ py: 3 }}>
          {selectedTab === 0 && (
            <Box>
              <Typography variant='h5' gutterBottom>
                API Overview
              </Typography>
              <Typography paragraph>
                EmbedIQ provides a REST API to upload documents, search for
                relevant information, and query using LLMs with RAG. All
                endpoints are available at the base URL:
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                }}
              >
                <code>http://api.embediq.example/api/v1</code>
              </Paper>

              <Typography variant='h6' gutterBottom sx={{ mt: 3 }}>
                Authentication
              </Typography>
              <Typography paragraph>
                All API requests require authentication using an API key.
                Include your API key in the request headers:
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                }}
              >
                <code>Authorization: Bearer YOUR_API_KEY</code>
              </Paper>

              <Typography variant='h6' gutterBottom sx={{ mt: 3 }}>
                Available Endpoints
              </Typography>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant='h6' color='primary'>
                    POST /ingest
                  </Typography>
                  <Typography>
                    Upload documents for embedding generation
                  </Typography>
                </CardContent>
              </Card>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant='h6' color='primary'>
                    GET/POST /search
                  </Typography>
                  <Typography>
                    Search for documents based on vector similarity
                  </Typography>
                </CardContent>
              </Card>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant='h6' color='primary'>
                    POST /query
                  </Typography>
                  <Typography>
                    Submit a natural language query and get a context-based
                    answer
                  </Typography>
                </CardContent>
              </Card>
              <Card>
                <CardContent>
                  <Typography variant='h6' color='primary'>
                    GET /health
                  </Typography>
                  <Typography>Check the health status of the API</Typography>
                </CardContent>
              </Card>
            </Box>
          )}

          {selectedTab === 1 && (
            <Box>
              <Typography variant='h5' gutterBottom>
                Document Ingestion
              </Typography>
              <Typography paragraph>
                The ingest endpoint allows you to upload documents for
                processing. Documents are processed asynchronously to generate
                embeddings for semantic search.
              </Typography>

              <Typography variant='h6' gutterBottom>
                Endpoint
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                }}
              >
                <code>POST /ingest</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Request Body
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "title": "Document Title",
  "source": "Optional Source",
  "author": "Optional Author",
  "content": "Full document content...",
  "metadata": {
    "optional": "metadata",
    "customField": "value"
  }
}`}</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Response
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "id": 123,
  "title": "Document Title",
  "source": "Optional Source",
  "author": "Optional Author",
  "created_at": "2023-08-15T14:32:21Z",
  "updated_at": "2023-08-15T14:32:21Z",
  "metadata": {
    "optional": "metadata",
    "customField": "value"
  }
}`}</code>
              </Paper>
            </Box>
          )}

          {selectedTab === 2 && (
            <Box>
              <Typography variant='h5' gutterBottom>
                Search
              </Typography>
              <Typography paragraph>
                The search endpoint allows you to find documents based on vector
                similarity to your query.
              </Typography>

              <Typography variant='h6' gutterBottom>
                Endpoint
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                }}
              >
                <code>POST /search</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Request Body
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "query": "Your search query",
  "top_k": 5,
  "filters": {
    "source": "Optional source filter",
    "author": "Optional author filter"
  }
}`}</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Response
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "query": "Your search query",
  "results": [
    {
      "document_id": 123,
      "document_title": "Document Title",
      "chunk_id": 456,
      "chunk_text": "Relevant text from the document...",
      "score": 0.92,
      "metadata": {
        "source": "Document Source",
        "author": "Document Author"
      }
    }
  ],
  "total": 10,
  "latency_ms": 42.5
}`}</code>
              </Paper>
            </Box>
          )}

          {selectedTab === 3 && (
            <Box>
              <Typography variant='h5' gutterBottom>
                Query
              </Typography>
              <Typography paragraph>
                The query endpoint allows you to ask natural language questions
                and receive AI-generated answers based on the context from your
                documents.
              </Typography>

              <Typography variant='h6' gutterBottom>
                Endpoint
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                }}
              >
                <code>POST /query</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Request Body
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "query": "Your natural language question",
  "context_filter": {
    "source": "Optional source filter"
  },
  "top_k": 5
}`}</code>
              </Paper>

              <Typography variant='h6' gutterBottom>
                Response
              </Typography>
              <Paper
                sx={{
                  p: 2,
                  mb: 3,
                  bgcolor: 'grey.100',
                  fontFamily: 'monospace',
                  overflowX: 'auto',
                  whiteSpace: 'pre',
                }}
              >
                <code>{`{
  "query": "Your natural language question",
  "answer": "AI-generated answer based on the retrieved context...",
  "context_chunks": [
    {
      "text": "Relevant text from document...",
      "document_id": 123,
      "chunk_id": 456,
      "score": 0.92
    }
  ],
  "sources": [
    {
      "title": "Document Title",
      "id": "123",
      "source": "Document Source",
      "author": "Document Author"
    }
  ],
  "latency_ms": 742.5
}`}</code>
              </Paper>
            </Box>
          )}
        </Box>
      </Box>
    </Container>
  );
}
