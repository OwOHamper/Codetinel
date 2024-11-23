import CustomPieChart from '@/components/CustomPieChart'
import VulnerabilitiesTable from '@/components/VulnerabilitiesTable'
import VulnerabilitiesTableFilter from '@/components/VulnerabilitiesTableFilter'

const data = [
  {
    name: "CWE-22",
    severity: "high",
    status: "detected",
  },
  {
    name: "CWE-22",
    severity: "medium",
    status: "detected",
  },
  {
    name: "CWE-22",
    severity: "critical",
    status: "detected",
  },
  {
    name: "CWE-22",
    severity: "medium",
    status: "detected",
  },
]

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
  return (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="grid items-center grid-cols-2 mb-4">
        <div>
          <p className="text-xl text-gray-600 font-bold">Project name</p>
          <h1 className="text-4xl font-black tracking-tight lg:text-5xl">Gigachat</h1>
        </div>

        <div className="block">
          <CustomPieChart chartData={chartData} chartConfig={chartConfig} />
        </div>
      </div>

      <VulnerabilitiesTableFilter />
      <VulnerabilitiesTable data={data} />
    </main>
  )
}
