import React from "react";
import { TriangleAlert, CircleCheck, Clock3, FlaskConical } from "lucide-react";


interface StatusProps {
    status: "detected" | "queued" | "pending" | "finished"; // Define the statuses
}

export default function StatusDisplay({ status }: StatusProps) {
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
        case "finished":
            Icon = CircleCheck;
            break;
    }

    return (
        <span className="flex items-center capitalize">
            <Icon className="mr-1 h-4 w-4" />
            {status}
        </span>
    )
}