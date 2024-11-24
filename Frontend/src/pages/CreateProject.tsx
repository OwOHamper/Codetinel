import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function CreateProject() {
  return (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="mt-20">
        <h1 className="text-4xl font-black tracking-tight lg:text-5xl text-indigo-600">Title</h1>
        <Input
          placeholder="Write the title of your project"
          className="peer w-full border-0 border-b-2 rounded-none border-indigo-600 focus:ring-0 focus:outline-none focus:border-indigo-800 hover:border-indigo-700 mt-5"
        />
        <style jsx>{`
  input:focus {
    outline: none !important;
    box-shadow: none !important;
  }
`}</style>

      </div>
      <div>
        <h1 className="text-4xl font-black tracking-tight lg:text-5xl mt-5 text-indigo-600">Insert data</h1>
        <Input type="text" placeholder="Write the url of your source code" className="mt-4 hover:bg-gray-100" />
        <Input type="text" placeholder="Write your project's deployment url" className="mt-2 hover:bg-gray-100" />
        <Input type="file" placeholder="Upload a .csv file with potential errors" className="mt-2 hover:bg-gray-100 py-1.5 h-full align-middle" />
      </div>
      <Button className="mt-4 bg-indigo-600 hover:bg-indigo-500">Create</Button>
    </main>
  )
}
