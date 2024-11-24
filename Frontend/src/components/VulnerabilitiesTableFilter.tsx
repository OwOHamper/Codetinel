import MultiSelect from "@/components/MultiSelect"
import { Button } from "@/components/ui/button"
import SeverityDisplay from "@/components/SeverityDipslay"
import StatusDisplay from "@/components/StatusDisplay"

interface VulnerabilitiesTableFilterProps {
  severity: string[]
  setSeverity: (severity: string[]) => void
  status: string[]
  setStatus: (status: string[]) => void
}

export default function VulnerabilitiesTableFilter({
  severity,
  setSeverity,
  status,
  setStatus
}: VulnerabilitiesTableFilterProps) {
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

            <Button className="bg-indigo-500 hover:bg-indigo-400">Test</Button>
        </div>
    )
}
