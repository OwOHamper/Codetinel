import clsx from "clsx"; // Optional for conditional classes

interface SeverityPillProps {
    severity: "low" | "medium" | "high" | "critical"; // Define the severity levels
}

function SeverityDisplay({ severity }: SeverityPillProps) {
    const pillStyles = clsx(
        "px-3 py-1 text-xs font-medium rounded-full capitalize inline-flex items-center justify-center", // Common pill styles
        {
            "bg-green-100 text-green-700": severity === "low",
            "bg-yellow-100 text-yellow-700": severity === "medium",
            "bg-orange-100 text-orange-700": severity === "high",
            "bg-red-100 text-red-700": severity === "critical",
        }
    )

    const dotStyles = clsx(
        "h-2 w-2 rounded-full mr-2", // Common pill styles
        {
            "bg-green-700": severity === "low",
            "bg-yellow-700": severity === "medium",
            "bg-orange-700": severity === "high",
            "bg-red-700": severity === "critical",
        }
    )

    return (
        <div className={pillStyles}>
            <div className={dotStyles} /> {/* Dot */}
            {severity}
        </div >
    )
}

export default SeverityDisplay

