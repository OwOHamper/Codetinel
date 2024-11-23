import { useState } from "react"
import MultiSelect from "@/components/MultiSelect"
import { Button } from "@/components/ui/button"
import SeverityDisplay from "./SeverityDipslay"

export default function VulnerabilitiesTableFilter() {
    const [severity, setSeverity] = useState([])
    const [status, setStatus] = useState([])

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
                        { value: "detected", label: "Detected" },
                        { value: "queued", label: "Queued" },
                        { value: "pending", label: "Pending" },
                        { value: "finished", label: "Finished" },
                    ]}
                    selected={status}
                    setSelected={setStatus}
                />
            </div>

            <Button>Test</Button>
        </div>
    )
}
