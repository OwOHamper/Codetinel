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

export default function Project() {
  return (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="mb-4">
        <p className="text-xl text-gray-600 font-bold">Project name</p>
        <h1 className="text-4xl font-black tracking-tight lg:text-5xl">Gigachat</h1>
      </div>

      <VulnerabilitiesTableFilter />
      <VulnerabilitiesTable data={data} />
    </main>
  )
}
