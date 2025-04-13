/* eslint-disable @typescript-eslint/no-explicit-any */
import type { ClassValue, HTMLButtonAttributes } from 'svelte/elements';

export const buttonColors = {
	black: 'bg-black text-white',
	red: 'bg-red text-white',
	green: 'bg-green text-white',
	accent: 'bg-accent text-white',
	primary: 'bg-primary text-white',
	'accent-light': 'bg-accent-light text-white'
};

export const buttonSizes = {
	base: 'px-6 py-4 text-[2rem] size-fit'
};

export const buttonShapes = {
	rounded: 'rounded-lg',
	pill: 'rounded-full'
};

export type tButtonMode = 'fill' | 'outline';

export type tButtonProps = HTMLButtonAttributes & {
	// Extra Props Here:
	buttonClass?: ClassValue;
	color?: keyof typeof buttonColors & any;
	size?: keyof typeof buttonSizes;
	mode?: tButtonMode;
	shape?: keyof typeof buttonShapes;
	text?: string;
	href?: string;
};
