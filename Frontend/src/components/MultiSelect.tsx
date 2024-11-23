import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";
import { ChevronDown } from "lucide-react"; // For the chevron icon
import { useEffect, useRef, useState } from "react";

export default function MultiSelect({ label, options, selected, setSelected }) {
    const [triggerWidth, setTriggerWidth] = useState(null); // Store trigger width
    const triggerRef = useRef(null); // Ref for PopoverTrigger

    useEffect(() => {
        const updateWidth = () => {
            if (triggerRef.current) {
                setTriggerWidth(triggerRef.current.offsetWidth);
            }
        };

        // Initial update
        updateWidth();

        // ResizeObserver for dynamic updates
        const resizeObserver = new ResizeObserver(() => {
            updateWidth();
        });

        if (triggerRef.current) {
            resizeObserver.observe(triggerRef.current);
        }

        return () => {
            resizeObserver.disconnect();
        };
    }, []);

    const toggleOption = (value) => {
        setSelected((prevSelected) =>
            prevSelected.includes(value)
                ? prevSelected.filter((v) => v !== value)
                : [...prevSelected, value]
        );
    };

    const renderSelected = () => {
        return options
            .filter((option) => selected.includes(option.value))
            .map((option) => option.element);
    };

    return (
        <div className="min-w-64">
            {/* Label */}
            <label className="block text-sm font-medium text-muted-foreground mb-1">
                {label}
            </label>

            <Popover>
                {/* Button with Chevron Icon */}
                <PopoverTrigger asChild>
                    <Button
                        ref={triggerRef}
                        variant="outline"
                        className={cn(
                            "w-full font-normal justify-between",
                            selected.length === 0 && "text-muted-foreground"
                        )}
                    >
                        <span className="flex items-center gap-1">
                            {selected.length === 0 ? "Select options" : renderSelected()}
                        </span>
                        <ChevronDown className="w-4 h-4 ml-2" />
                    </Button>
                </PopoverTrigger>

                {/* Dropdown Menu */}
                <PopoverContent
                    className="w-64 left-0 p-1"
                    style={{ width: triggerWidth }}
                >
                    {options.map((option) => (
                        <div
                            key={option.value}
                            onClick={() => toggleOption(option.value)}
                            className="flex items-center gap-2 px-2 py-1 rounded cursor-pointer hover:bg-gray-100"
                        >
                            <Checkbox
                                id={option.value}
                                checked={selected.includes(option.value)}
                            />

                            {option.element}
                        </div>
                    ))}
                </PopoverContent>
            </Popover>
        </div>
    );
}
