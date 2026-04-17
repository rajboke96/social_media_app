import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { ApolloProvider } from "@apollo/client/react";
import { client } from './lib/apolloClient.js';
import "./index.css"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </StrictMode>,
)

// client.mutate(gql`
// mutation MyMutation {
//   login(data: {username: "rajendra.boke", password: "raj@123"})
// }
// `)