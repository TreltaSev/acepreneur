import type { HTMLAttributes } from "svelte/elements";

export type tFlexProps = HTMLAttributes<HTMLDivElement> & {
    el?: HTMLDivElement
};