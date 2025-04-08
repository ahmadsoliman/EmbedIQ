import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';

/**
 * 404 Not Found page
 */
function NotFoundPage() {
  return (
    <Container maxWidth='lg'>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          py: 8,
          textAlign: 'center',
        }}
      >
        <Typography variant='h1' component='h1' color='primary' gutterBottom>
          404
        </Typography>
        <Typography variant='h4' component='h2' gutterBottom>
          Page Not Found
        </Typography>
        <Typography color='text.secondary' paragraph>
          The page you are looking for does not exist or has been moved.
        </Typography>
        <Button
          variant='contained'
          component={RouterLink}
          to='/'
          sx={{ mt: 4 }}
        >
          Return to Home
        </Button>
      </Box>
    </Container>
  );
}

export default NotFoundPage;
