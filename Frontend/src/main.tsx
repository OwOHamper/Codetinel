import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from 'react-query';

// Import pages
import Projects from '@/pages/Projects';
import CreateProject from '@/pages/CreateProject';
import Project from '@/pages/Project';
import Detail from './pages/Detail';

// Create a client instance
const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <img src="/logo.png" alt="logo" className="w-24 h-24 absolute top-0 left-4" />
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/projects" replace />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/new" element={<CreateProject />} />
          <Route path="/projects/:projectId" element={<Project />} />
          <Route path="/projects/:projectId/error/:errorId" element={<Detail />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  </StrictMode>,
)
