import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { client } from './lib/apolloClient.js';
import "./index.css"

createRoot(document.getElementById('root')).render(
  <StrictMode>
      <App />
  </StrictMode>,
)