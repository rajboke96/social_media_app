import { ApolloClient, HttpLink, InMemoryCache } from '@apollo/client'

const graphqlUri = import.meta.env.VITE_GRAPHQL_URL

export const client = new ApolloClient({
    link: new HttpLink({ 
      uri: graphqlUri,
      credentials: 'include',
    }),
    cache: new InMemoryCache(),
  });