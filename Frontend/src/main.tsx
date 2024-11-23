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
import CreateProject from '@/pages/CreateProject';
import Project from '@/pages/Project';
import Detail from './pages/Detail';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/new" element={<CreateProject />} />
        <Route path="/projects/:projectId" element={<Project />} />
        <Route path="/projects/:projectId/error/:errorId" element={<Detail />} />
      </Routes>
    </Router>
  </StrictMode>,
)
