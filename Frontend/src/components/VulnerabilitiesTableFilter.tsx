import { useState } from "react"
import MultiSelect from "@/components/MultiSelect"
import { Button } from "@/components/ui/button"
import SeverityDisplay from "./SeverityDipslay"

export default function VulnerabilitiesTableFilter() {
    const [severity, setSeverity] = useState([])
    const [status, setStatus] = useState([])

    return (
        <div className="flex gap-2 items-end mb-4">
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
                    { value: "option1", label: "Option 1" },
                    { value: "option2", label: "Option 2" },
                    { value: "option3", label: "Option 3" },
                ]}
                selected={status}
                setSelected={setStatus}
            />

            <Button>Test</Button>
        </div>
    )
}
