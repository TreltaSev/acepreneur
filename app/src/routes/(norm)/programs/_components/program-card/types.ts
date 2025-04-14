import type { Program } from "@internal/types";
import type { ClassValue, HTMLAttributes } from "svelte/elements";

export type tProgramCardProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    programCardClass?: ClassValue,
    
    // Extra Props Here:
    data?: Program,
};