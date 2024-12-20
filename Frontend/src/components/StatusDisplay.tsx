import { TriangleAlert, CircleCheck, Loader2, CircleX } from "lucide-react";


interface StatusProps {
    status: "failed" | "processing" | "completed" | "not_started"; // Define the statuses
}

function StatusDisplay({ status }: StatusProps) {
    let Icon;
    switch (status) {
        case "failed":
            Icon = CircleX;
            break;
        case "processing":
            Icon = Loader2;
            break;
        case "completed":
            Icon = CircleCheck;
            break;
        case "not_started":
            Icon = TriangleAlert;
            break;
    }

    return (
        <div className="flex items-center capitalize">
            {Icon && <Icon className={`mr-1 h-4 w-4 ${status === "completed" ? "text-green-500" : ""}
                ${status === "failed" ? "text-red-500" : ""}
                ${status === "not_started" ? "text-yellow-500" : ""}
                ${status === "processing" ? "animate-spin" : ""}`} />}
            {status.replace('_', ' ')}
        </div>
    )
}

export default StatusDisplay
