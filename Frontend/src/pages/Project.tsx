import VulnerabilitiesTable from '@/components/VulnerabilitiesTable'
import VulnerabilitiesTableFilter from '@/components/VulnerabilitiesTableFilter'
import React from 'react'

const data = [
  {
    name: "CWE-22",
    severity: "medium",
    status: "detected",
  },
  {
    name: "CWE-22",
    severity: "medium",
    status: "detected",
  },
  {
    name: "CWE-22",
    severity: "medium",
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
    <div>
      Project
      <VulnerabilitiesTableFilter />
      <VulnerabilitiesTable data={data} />
    </div>
  )
}
