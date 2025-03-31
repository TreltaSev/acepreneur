import type { ClassValue, HTMLAttributes } from "svelte/elements";

export type tFlexProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    flexClass?: ClassValue,
    
    // Extra Props Here:

};
export type tFlexColProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    colClass?: ClassValue,
    
    // Extra Props Here:
};
export type tFlexRowProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    rowClass?: ClassValue,
    
    // Extra Props Here:
};