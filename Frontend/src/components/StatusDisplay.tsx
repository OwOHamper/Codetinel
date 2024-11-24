import { TriangleAlert, CircleCheck, Clock3, FlaskConical } from "lucide-react";


interface StatusProps {
    status: "detected" | "queued" | "pending" | "completed" | "not_started"; // Define the statuses
}

function StatusDisplay({ status }: StatusProps) {
    let Icon;
    switch (status) {
        case "detected":
            Icon = TriangleAlert;
            break;
        case "queued":
            Icon = Clock3;
            break;
        case "pending":
            Icon = FlaskConical;
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
            <Icon className="mr-1 h-4 w-4" />
            {status}
        </div>
    )
}

export default StatusDisplay
