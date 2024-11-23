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
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
  { browser: "firefox", visitors: 287, fill: "var(--color-firefox)" },
  { browser: "edge", visitors: 173, fill: "var(--color-edge)" },
  { browser: "other", visitors: 190, fill: "var(--color-other)" },
]

const chartConfig = {
  visitors: {
    label: "Visitors",
  },
  chrome: {
    label: "Chrome",
    color: "hsl(var(--chart-1))",
  },
  safari: {
    label: "Safari",
    color: "hsl(var(--chart-2))",
  },
  firefox: {
    label: "Firefox",
    color: "hsl(var(--chart-3))",
  },
  edge: {
    label: "Edge",
    color: "hsl(var(--chart-4))",
  },
  other: {
    label: "Other",
    color: "hsl(var(--chart-5))",
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
