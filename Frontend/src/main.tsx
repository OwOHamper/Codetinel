import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

// Import pages

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Router>
      <Routes>

      </Routes>
    </Router>
  </StrictMode>,
)
