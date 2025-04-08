import type { Event } from "@internal/types";
import type { ClassValue, HTMLAttributes } from "svelte/elements";

export type tEventCardProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    eventCardClass?: ClassValue,
    
    // Extra Props Here:
    data?: Event
};