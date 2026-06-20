import { ApolloClient, HttpLink, InMemoryCache } from '@apollo/client'

const graphqlUri = import.meta.env.VITE_GRAPHQL_URL || "http://127.0.0.1:8000/graphql"

export const client = new ApolloClient({
    link: new HttpLink({ 
      uri: graphqlUri,
      credentials: 'include',
    }),
    cache: new InMemoryCache(),
  });