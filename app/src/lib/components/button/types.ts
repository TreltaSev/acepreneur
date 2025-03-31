import type { ClassValue, HTMLButtonAttributes } from "svelte/elements";

export const buttonColors = {
    "black": "bg-black text-white",
    "red": "bg-red text-white",
    "green": "bg-green text-white",
    "accent": "bg-accent text-white",
    "primary": "bg-primary text-white",
    "accent-light": "bg-accent-light text-white"
}

export const buttonSizes = {
    "base": "px-9 py-3 s_sm:py-5 s_xs:py-6 s_xs:text-lg s_sm:text-md"
}

export type tButtonProps = HTMLButtonAttributes & {
    // Extra Props Here:
    buttonClass?: ClassValue ,
    color?: keyof typeof buttonColors,
    size?: keyof typeof buttonSizes
};