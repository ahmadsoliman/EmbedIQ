import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
  Container,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import CodeIcon from '@mui/icons-material/Code';
import StorageIcon from '@mui/icons-material/Storage';

/**
 * Home page with introduction and feature highlights
 */
function HomePage() {
  const navigate = useNavigate();

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          textAlign: 'center',
          py: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography variant='h2' component='h1' gutterBottom>
          Welcome to EmbedIQ
        </Typography>
        <Typography
          variant='h5'
          color='text.secondary'
          paragraph
          sx={{ maxWidth: 700, mb: 4 }}
        >
          A powerful RAG system that combines vector embeddings with LLM
          capabilities to provide context-aware AI responses for your documents.
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant='contained'
            size='large'
            onClick={() => navigate('/query')}
            sx={{ mx: 1 }}
          >
            Try the Query Interface
          </Button>
          <Button
            variant='outlined'
            size='large'
            onClick={() => navigate('/docs')}
            sx={{ mx: 1 }}
          >
            API Documentation
          </Button>
        </Box>
      </Box>

      {/* Features Section */}
      <Container sx={{ py: 8 }} maxWidth='md'>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <SearchIcon fontSize='large' color='primary' />
                </Box>
                <Typography variant='h5' component='h2' gutterBottom>
                  High-Quality Search
                </Typography>
                <Typography>
                  Utilize advanced vector embedding search to find the most
                  relevant information in your document collection.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <StorageIcon fontSize='large' color='primary' />
                </Box>
                <Typography variant='h5' component='h2' gutterBottom>
                  Context-Aware LLM
                </Typography>
                <Typography>
                  Get AI-generated answers that are informed by the context from
                  your documents, with source attribution.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <CodeIcon fontSize='large' color='primary' />
                </Box>
                <Typography variant='h5' component='h2' gutterBottom>
                  Developer-Friendly API
                </Typography>
                <Typography>
                  Integrate EmbedIQ's capabilities into your applications with
                  our comprehensive API and documentation.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default HomePage;
