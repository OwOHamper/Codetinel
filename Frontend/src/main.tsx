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
      <div className="flex items-center fixed top-1 left-2">
        <img src="/logo.png" alt="logo" className="w-16 h-16" />
        <p className="-ml-3 text-2xl font-black tracking-tight text-indigo-700">Codetinel</p>
      </div>
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
