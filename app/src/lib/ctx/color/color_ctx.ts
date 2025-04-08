/* eslint-disable @typescript-eslint/no-explicit-any */

import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';

/**
 * Creates a new writable store for holding a color value.
 * This color value is expected to be a string (e.g., hex code) or `null`.
 * @returns An object containing the writable store `color$`.
 */
export function createColorData() {
	const color$: Writable<string | null> = writable(null);

	return {
		color$
	};
}

/**
 * Provides a constant name used as the key for Svelte context.
 * This avoids hardcoding the string multiple times.
 * @returns An object containing the `NAME` identifier for the color context.
 */
export function getColorData() {
	const NAME = 'color-data' as const;
	return {
		NAME
	};
}

/**
 * Initializes and sets the color context for the app.
 * Should be called once in a root component like `+layout.svelte`.
 * @returns The initialized color store object, useful for local access.
 */
export function setColorCtx() {
	const { NAME } = getColorData();

	const color = {
		...createColorData()
	};

	setContext(NAME, color);

	return {
		...color
	};
}

// Define the return type of `setColorCtx` for use with `getContext`
type GetColorReturn = ReturnType<typeof setColorCtx>;

/**
 * Retrieves the color context previously set via `setColorCtx()`.
 * This is used to access or update the global color accent used throughout the app,
 * typically for UI theming like button highlights or component accents.
 * @returns The color context object containing the `color$` writable store.
 */
export function getColorCtx() {
	const { NAME } = getColorData();
	return getContext<GetColorReturn>(NAME);
}
