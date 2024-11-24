import { Loader2, Plus } from "lucide-react"
import { Link } from "react-router-dom"
import { useQuery } from "react-query"
import axios from "axios"

interface Project {
  _id: string
  project_name: string
}

export default function Projects() {
  const { data: projects, status } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/project/get_all_projects`)
      return response.data
    }
  })

  if (status === 'loading') {
    return (
      <div className="h-screen flex justify-center items-center">
        <Loader2 className='my-28 h-16 w-16 text-primary/60 animate-spin' />
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="h-screen flex justify-center items-center">
        <p>An error has occurred!</p>
      </div>
    )
  }

  return (
    <main className="max-w-screen-lg mx-auto px-4 py-8">
      <div className="mb-12">
        <p className="text-xl text-indigo-600 font-bold">Welcome, Jožko!</p>
        <h1 className="text-4xl text-indigo-800 font-black tracking-tight lg:text-5xl">What projects can we analyse today?</h1>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Link to="/projects/new" className="border-2 border-indigo-600 h-44 rounded-xl flex items-center justify-center hover:bg-indigo-50">
          <Plus className="w-12 h-12 text-indigo-600" />
        </Link>
        {projects?.map((project: Project) => (
          <Link 
            key={project._id}
            to={`/projects/${project._id}`} 
            className="border-2 border-indigo-600 h-44 rounded-xl flex items-center justify-center hover:bg-indigo-50"
          >
            <span className="text-indigo-600 text-2xl">{project.project_name}</span>
          </Link>
        ))}
      </div>
    </main>
  )
}
