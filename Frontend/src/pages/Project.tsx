import CustomPieChart from '@/components/CustomPieChart'
import VulnerabilitiesTable from '@/components/VulnerabilitiesTable'
import VulnerabilitiesTableFilter from '@/components/VulnerabilitiesTableFilter'
import { Loader2 } from 'lucide-react'
import { useQuery } from 'react-query'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { useState } from 'react'

const chartConfig = {
  visitors: {
    label: "Count",
  },
  critical: {
    label: "Critical",
    color: "#f87171",
  },
  high: {
    label: "High",
    color: "#fb923c",
  },
  medium: {
    label: "Medium",
    color: "#facc15",
  },
  low: {
    label: "Low",
    color: "#4ade80",
  },
}

export default function Project() {
  const { projectId } = useParams()
  const [severity, setSeverity] = useState<string[]>([])
  const [status, setStatus] = useState<string[]>([])

  const fetchProject = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/project/get_project/${projectId}`)
      return response.data
    } catch (error) {
      console.error(error)
    }
  }

  const { data, status: queryStatus } = useQuery({
    queryKey: ['project', projectId],
    queryFn: fetchProject,
  })

  const filteredData = data ? Object.values(data.vulnerabilities).filter((item: any) => {
    const severityMatch = severity.length === 0 || severity.includes(item.severity)
    const statusMatch = status.length === 0 || status.includes(item.status)
    return severityMatch && statusMatch
  }) : []

  const getChartData = (data: any[]) => {
    const severityCounts = {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
    }

    data.forEach((item: any) => {
      const severity = item.severity.toLowerCase()
      if (severity in severityCounts) {
        severityCounts[severity as keyof typeof severityCounts]++
      }
    })

    return [
      { browser: "critical", visitors: severityCounts.critical, fill: "#f87171" },
      { browser: "high", visitors: severityCounts.high, fill: "#fb923c" },
      { browser: "medium", visitors: severityCounts.medium, fill: "#facc15" },
      { browser: "low", visitors: severityCounts.low, fill: "#4ade80" },
    ]
  }

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
          <h1 className="text-4xl text-indigo-800 font-black tracking-tight lg:text-5xl">{data.project_name}</h1>
        </div>

        <div className="block">
          <CustomPieChart 
            chartData={getChartData(Object.values(data.vulnerabilities))} 
            chartConfig={chartConfig} 
          />
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
