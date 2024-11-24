import CustomPieChart from '@/components/CustomPieChart'
import VulnerabilitiesTable from '@/components/VulnerabilitiesTable'
import VulnerabilitiesTableFilter from '@/components/VulnerabilitiesTableFilter'
import { Loader2 } from 'lucide-react'
import { useQuery } from 'react-query'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { useState } from 'react'

const chartData = [
  { browser: "critical", visitors: 275, fill: "#f87171" },
  { browser: "high", visitors: 200, fill: "#fb923c" },
  { browser: "medium", visitors: 287, fill: "#facc15" },
  { browser: "low", visitors: 173, fill: "#4ade80" },
]

const chartConfig = {
  visitors: {
    label: "Visitors",
  },
  critical: {
    label: "Chrome",
    color: "#f87171",
  },
  high: {
    label: "Safari",
    color: "#fb923c",
  },
  medium: {
    label: "Firefox",
    color: "#facc15",
  },
  low: {
    label: "Edge",
    color: "#4ade80",
  },
}

export default function Project() {
  const { projectId } = useParams()
  const [severity, setSeverity] = useState<string[]>([])
  const [status, setStatus] = useState<string[]>([])

  const fetchProject = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/vulnerabilities/get-vulnerabilities/${projectId}`)
      return response.data
    } catch (error) {
      console.error(error)
    }
  }

  const { data, status: queryStatus } = useQuery({
    queryKey: ['project', projectId],
    queryFn: fetchProject,
  })

  const filteredData = data ?  Object.values(data).filter((item: any) => {
    const severityMatch = severity.length === 0 || severity.includes(item.severity)
    const statusMatch = status.length === 0 || status.includes(item.status)
    return severityMatch && statusMatch
  }) : []

  return queryStatus === "loading" ? (
    <div className="h-screen flex justify-center items-center">
      <Loader2
        className='my-28 h-16 w-16 text-primary/60 animate-spin'
      />
    </div>
  ) : queryStatus === "error" ? (
    <div className="h-screen flex justify-center items-center">
      <p>An error has occured!</p>
    </div>
  ) : data ? (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="grid items-center grid-cols-2 mb-4">
        <div>
          <p className="text-xl text-indigo-600 font-bold">Project name</p>
          <h1 className="text-4xl text-indigo-800 font-black tracking-tight lg:text-5xl"></h1>
        </div>

        <div className="block">
          <CustomPieChart chartData={chartData} chartConfig={chartConfig} />
        </div>
      </div>

      <VulnerabilitiesTableFilter 
        severity={severity}
        setSeverity={setSeverity}
        status={status}
        setStatus={setStatus}
      />
      <VulnerabilitiesTable data={filteredData} />
    </main>
  ) : null
}
