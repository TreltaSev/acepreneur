import type { ClassValue, HTMLAttributes } from "svelte/elements";

export type tToggleProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    toggleClass?: ClassValue,
    
    // Extra Props Here:
    value?: boolean

    // Callback Functions
    onupdate?: (value: boolean) => void;
    ontrue?: () => void;
    onfalse?: () => void;
};