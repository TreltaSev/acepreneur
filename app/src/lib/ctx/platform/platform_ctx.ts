/* eslint-disable @typescript-eslint/no-explicit-any */
import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import { Capacitor } from '@capacitor/core';

/**
 * Wrapper function for `Capacitor.getPlatform()` that returns the correct type
 * @returns Platform
 */
function getPlatformWrapper() {
	return Capacitor.getPlatform() as 'web' | 'ios' | 'android';
}

export function createPlatformData() {
	const platform$: Writable<ReturnType<typeof getPlatformWrapper>> = writable(getPlatformWrapper());

	return {
		platform$
	};
}

export function getPlatformData() {
	const NAME = 'platform-data' as const;

	return {
		NAME
	};
}

export function setPlatformCtx() {
	const { NAME } = getPlatformData();

	const platform = {
		...createPlatformData()
	};

	setContext(NAME, platform);

	return {
		...platform
	};
}

type GetPlatformReturn = ReturnType<typeof setPlatformCtx>;
export function getPlatformCtx() {
	const { NAME } = getPlatformData();
	return getContext<GetPlatformReturn>(NAME);
}
