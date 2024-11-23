import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

// Import pages
import Projects from '@/pages/Projects';
import Project from '@/pages/Project';
import CreateProject from '@/pages/CreateProject';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/:projectId" element={<Project />} />
        <Route path="/projects/new" element={<CreateProject />} />
      </Routes>
    </Router>
  </StrictMode>,
)
