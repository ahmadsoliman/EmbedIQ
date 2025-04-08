import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';

// Layout components
import Layout from './components/Layout';

// Page components
import HomePage from './pages/HomePage';
import QueryPage from './pages/QueryPage';
import DocsPage from './pages/DocsPage';
import NotFoundPage from './pages/NotFoundPage';

/**
 * Main App component that defines the application routes
 */
function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path='query' element={<QueryPage />} />
          <Route path='docs' element={<DocsPage />} />
          <Route path='*' element={<NotFoundPage />} />
        </Route>
      </Routes>
    </Box>
  );
}

export default App;
