import { Plus } from "lucide-react"
import { Link } from "react-router-dom"

export default function Projects() {
  return (
    <main className="max-w-screen-lg mx-auto px-4 py-8">
      <div className="mb-12">
        <p className="text-xl text-indigo-600 font-bold">Welcome, Jožko!</p>
        <h1 className="text-4xl text-indigo-800 font-black tracking-tight lg:text-5xl">What projects can we analyse today?</h1>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Link to="/projects/new" className="border-2 border-indigo-600 h-44 rounded-xl flex items-center justify-center hover:bg-indigo-50">
          <Plus className="w-12 h-12 text-indigo-600" />
          {/* <span className="text-indigo-600 text-2xl">+</span> */}
        </Link>
        <Link to="/projects/id" className="border-2 border-indigo-600 h-44 rounded-xl flex items-center justify-center hover:bg-indigo-50 relative">
          <span className="text-indigo-600 text-2xl">Gigachat</span>
        </Link>
        <Link to="/projects/id" className="border-2 border-indigo-600 h-44 rounded-xl flex items-center justify-center hover:bg-indigo-50">
          <span className="text-indigo-600 text-2xl">Lorem Ipsum</span>
        </Link>
      </div>
    </main>
  )
}
