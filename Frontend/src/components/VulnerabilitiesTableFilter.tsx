import MultiSelect from "@/components/MultiSelect"
import { Button } from "@/components/ui/button"
import SeverityDisplay from "@/components/SeverityDipslay"
import StatusDisplay from "@/components/StatusDisplay"
import axios from "axios"
import { useQueryClient } from "react-query"

interface VulnerabilitiesTableFilterProps {
  severity: string[]
  setSeverity: (severity: string[]) => void
  status: string[]
  setStatus: (status: string[]) => void
  selectedVulnerabilities: string[]
  projectId: string
}

export default function VulnerabilitiesTableFilter({
  severity,
  setSeverity,
  status,
  setStatus,
  selectedVulnerabilities,
  projectId,
}: VulnerabilitiesTableFilterProps) {
    const queryClient = useQueryClient()

    const handleTest = async () => {
        try {
            // Start all tests
            for (const vulnId of selectedVulnerabilities) {
                await axios.post(`${import.meta.env.VITE_API_URL}/api/agent/pentest/test`, {
                    project_id: projectId,
                    vulnerability_id: vulnId
                })
            }

            // Poll for changes every 2 seconds for up to 1 minute
            const pollInterval = 2000 // 2 seconds
            const maxAttempts = 30    // 1 minute total
            let attempts = 0

            const pollForChanges = async () => {
                while (attempts < maxAttempts) {
                    await new Promise(resolve => setTimeout(resolve, pollInterval))
                    await queryClient.invalidateQueries(['project', projectId])
                    attempts++
                }
            }

            // Start polling in the background
            pollForChanges()
        } catch (error) {
            console.error('Error testing vulnerabilities:', error)
        }
    }

    return (
        <div className="flex gap-2 items-end justify-between mb-4">
            <div className="flex items-center gap-2">
                <MultiSelect
                    label="Severity"
                    options={[
                        { value: "critical", element: <SeverityDisplay severity="critical" /> },
                        { value: "high", element: <SeverityDisplay severity="high" /> },
                        { value: "medium", element: <SeverityDisplay severity="medium" /> },
                        { value: "low", element: <SeverityDisplay severity="low" /> },
                    ]}
                    selected={severity}
                    setSelected={setSeverity}
                />
                <MultiSelect
                    label="Status"
                    options={[
                        { value: "not_started", element: <StatusDisplay status="not_started" /> },
                        { value: "queued", element: <StatusDisplay status="queued" /> },
                        { value: "pending", element: <StatusDisplay status="pending" /> },
                        { value: "completed", element: <StatusDisplay status="completed" /> },
                    ]}
                    selected={status}
                    setSelected={setStatus}
                />
            </div>

            <Button 
                className="bg-indigo-500 hover:bg-indigo-400"
                onClick={handleTest}
                disabled={selectedVulnerabilities.length === 0}
            >
                Test
            </Button>
        </div>
    )
}
