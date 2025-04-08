import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, Container } from '@mui/material';

import Header from './Header';
import Footer from './Footer';

/**
 * Layout component that wraps all pages with a consistent header and footer
 */
function Layout() {
  return (
    <>
      <Header />
      <Box
        component='main'
        sx={{
          flexGrow: 1,
          py: 4,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Container maxWidth='lg' sx={{ flexGrow: 1 }}>
          <Outlet />
        </Container>
      </Box>
      <Footer />
    </>
  );
}

export default Layout;
