import type { ClassValue, HTMLAttributes } from "svelte/elements";

export type tProgramLinkProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    programLinkClass?: ClassValue,
    
    // Extra Props Here:
    slug?: string
};