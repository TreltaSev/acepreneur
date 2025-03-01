import type { HTMLButtonAttributes } from "svelte/elements";

export type tButtonProps = HTMLButtonAttributes & {
    href?: string;
    newPage?: boolean;
}