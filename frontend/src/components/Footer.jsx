import React from 'react';
import { Box, Container, Typography, Link, Divider } from '@mui/material';

/**
 * Footer component with copyright and links
 */
function Footer() {
  return (
    <Box
      component='footer'
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[100],
      }}
    >
      <Divider />
      <Container maxWidth='lg'>
        <Box
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', md: 'row' },
            justifyContent: 'space-between',
            alignItems: 'center',
            mt: 2,
          }}
        >
          <Typography variant='body2' color='text.secondary'>
            {'© '}
            {new Date().getFullYear()}
            {' EmbedIQ. All rights reserved.'}
          </Typography>
          <Box
            sx={{
              display: 'flex',
              gap: 2,
              mt: { xs: 2, md: 0 },
            }}
          >
            <Link href='#' color='inherit' underline='hover'>
              Privacy Policy
            </Link>
            <Link href='#' color='inherit' underline='hover'>
              Terms of Service
            </Link>
            <Link href='#' color='inherit' underline='hover'>
              Contact
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}

export default Footer;
