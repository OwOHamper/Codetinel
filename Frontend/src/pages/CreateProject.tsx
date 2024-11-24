import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Pencil, Link, CloudUpload } from "lucide-react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function CreateProject() {
  const navigate = useNavigate()
  const [title, setTitle] = useState("")
  const [deployUrl, setDeployUrl] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [url, setUrl] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append("project_name", title)
      formData.append("deployment_url", url)
      formData.append("url", deployUrl)
      if (file) formData.append("csv_file", file)

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/project/create`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )

      navigate(`/projects/${response.data.project_id}`, { replace: true })
    } catch (error: any) {
      console.log("Failed to create project: " + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const isFormValid = title && deployUrl && file && !isLoading

  return (
    <form onSubmit={handleSubmit} className="max-w-screen-lg mx-auto p-4">
      <div className="mt-20">
        <h1 className="text-4xl font-black tracking-tight lg:text-5xl text-indigo-600">Title</h1>
        <div className="relative">
          <Input
            placeholder="Write the title of your project"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="peer w-full border-0 border-b-2 rounded-none border-indigo-600 focus:ring-0 focus:outline-none focus:border-indigo-800 hover:border-indigo-700 mt-5 pl-9"
          />
          <style jsx>{`
            input:focus {
              outline: none !important;
              box-shadow: none !important;
            }
          `}</style>
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
            <Pencil className="h-4 w-4" />
          </span>
        </div>
      </div>

      <div>
        <h1 className="text-4xl font-black tracking-tight lg:text-5xl mt-5 text-indigo-600">Insert data</h1>

          <div className="relative">
            <Input
              type="text"
              placeholder="Write the url of your source code"
              value={deployUrl}
              onChange={(e) => setDeployUrl(e.target.value)}
              className="mt-4 hover:bg-gray-100 pl-9"
            />
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
              <Link className="h-4 w-4" />
            </span>
          </div>

          <div className="relative">
            <Input
              type="text"
              placeholder="Write the url of the deployment which should be tested on"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="mt-2 hover:bg-gray-100 pl-9"
            />
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
              <Link className="h-4 w-4" />
            </span>
          </div>

        <div className="relative">
          <Input
            type="file"
            placeholder="Upload a .csv file with potential errors"
            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
            className="mt-2 hover:bg-gray-100 py-1.5 h-full align-middle pl-9"
          />
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 align-middle">
            <CloudUpload className="h-4 w-4" />
          </span>
        </div>
      </div>

      <Button
        type="submit"
        className="mt-4 bg-indigo-600 hover:bg-indigo-500"
        disabled={!isFormValid}
      >
        {isLoading ? "Creating..." : "Create"}
      </Button>
    </form>
  )
}

