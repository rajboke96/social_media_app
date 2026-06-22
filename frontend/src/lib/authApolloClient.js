import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
// ✅ Import the official, robust upload link module
import createUploadLink from 'apollo-upload-client/UploadHttpLink.mjs';

const authGraphqlUri = import.meta.env.VITE_AUTH_GRAPHQL_URL || 'http://localhost:8000/auth/graphql';
const appGraphqlUri = import.meta.env.VITE_APP_GRAPHQL_URL || 'http://localhost:8000/app/graphql'; // Fixed env typo from VITE_AUTH_GRAPHQL_URL

// --- 🔐 1. AUTH CLIENT CONFIGURATION (Standard JSON) ---
export const authClient = new ApolloClient({
  link: createHttpLink({
    uri: authGraphqlUri,
    credentials: 'include', // Includes cookies automatically
  }),
  cache: new InMemoryCache(),
});

// --- 📦 2. APP CLIENT CONFIGURATION (Handles JSON + Image Uploads) ---
// createUploadLink acts as a terminating HttpLink that transforms requests automatically
const uploadLink = new createUploadLink({
  uri: appGraphqlUri,
  credentials: 'include', // Includes cookies for your app queries
  headers: {
    'Apollo-Require-Preflight': 'true', // Recommended security layout
  }
});

// Context link to dynamically read tokens if your backend uses Bearer authentication
const authMiddleware = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

export const appClient = new ApolloClient({
  link: authMiddleware.concat(uploadLink),
  cache: new InMemoryCache(),
});