import { TriangleAlert } from 'lucide-react'

export default function Detail() {
  return (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="grid items-center mb-8">
        <p className="text-xl text-gray-600 font-bold">CWE-22</p>
        <h1 className="text-4xl font-black tracking-tight">Improper limitation of a pathname to a restricted directory ('Path Traversal')</h1>
      </div>

      <div className="flex items-center gap-2 mb-4">
        <TriangleAlert className="bg-indigo-600 text-white rounded-lg p-2 w-10 h-10" />
        <p className="font-bold text-2xl text-indigo-600">Summary of the Vulnerabilitie</p>
      </div>
      <p className="mb-8">Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum culpa cumque quam nesciunt magnam fuga id labore quas aliquid veniam possimus, quis molestias ea architecto ad incidunt illo qui. Praesentium.</p>

        <p className="font-bold text-2xl text-indigo-600 mb-4">Step by step overview</p>
      <div className="border border-black rounded-lg p-4">

      </div>
    </main>
  )
}
