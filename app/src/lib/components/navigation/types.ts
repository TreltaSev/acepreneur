import type { Snippet } from "svelte";
import type { ClassValue, HTMLAnchorAttributes, HTMLAttributes } from "svelte/elements";

export type tNavigationProps = HTMLAttributes<HTMLDivElement> & {
    // Classes:

    // --- Default Classes:
    navigationClass?: ClassValue,
    
    // Extra Props Here:

};
export type tNavigationItemProps = HTMLAnchorAttributes & {
    // Classes:

    // --- Default Classes:
    itemClass?: ClassValue,
    iconClass?: ClassValue,

    // --- User Defined Classes:
    classIcon?: ClassValue,
    
    // Extra Props Here:
    href?: string,

    // Snippets Here:
    icon?: Snippet
};