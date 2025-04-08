# EmbedIQ Frontend

This directory contains the frontend React application for the EmbedIQ RAG system.

## Features

- Modern React application with functional components and hooks
- Material-UI for consistent and responsive design
- React Router for navigation
- React Query for data fetching and caching
- Vite for fast development and building

## Directory Structure

```
/frontend
├── public/         # Static assets
├── src/            # Source code
│   ├── components/ # Reusable components
│   ├── pages/      # Page components
│   ├── services/   # API client and services
│   ├── utils/      # Utility functions
│   ├── App.jsx     # Main app component
│   ├── main.jsx    # Entry point
│   └── theme.js    # Theme configuration
├── .eslintrc.js    # ESLint configuration
├── Dockerfile      # Container definition
├── nginx.conf      # Nginx configuration for production
├── package.json    # Dependencies and scripts
└── vite.config.js  # Vite configuration
```

## Getting Started

### Running Locally

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

This will start the development server at http://localhost:3000.

### Building for Production

```bash
npm run build
```

This will create a production build in the `dist` directory.

## Development

### Adding New Components

1. Create a new component in `src/components/` or `src/pages/`
2. Import and use the component where needed
3. Use Material-UI components for consistent design

### API Integration

API calls should be abstracted into service functions in `src/services/`:

```jsx
// Example in src/services/api.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const searchDocuments = async (query) => {
  const response = await axios.post(`${API_URL}/search`, { query });
  return response.data;
};
```

### Adding New Routes

1. Create a new page component in `src/pages/`
2. Add the route in `src/App.jsx`

```jsx
<Route path='/new-page' element={<NewPage />} />
```

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run lint`: Run ESLint
- `npm run preview`: Preview production build locally
