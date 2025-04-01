/* eslint-disable @typescript-eslint/no-explicit-any */
import { getContext, setContext } from 'svelte';
import { get, writable, type Writable } from 'svelte/store';

export function createIdentificationData() {
	const identity$: Writable<string | null> = writable(null);

	identity$.subscribe((current_identity) => {
		if (!current_identity) return;

		console.info("Update identity")
		localStorage.setItem("identification", current_identity)
	})

	setInterval(() => {
		if (typeof window === 'undefined' || !localStorage) return;
		try {
			const userIdentification = localStorage.getItem('identification');
			if (get(identity$) != userIdentification) {
				identity$.set(userIdentification);
			}
		} catch (error) {
			console.warn(`Error`, error);
			return;
		}
	}, 10);

	return {
		x$: identity$
	};
}

export function getIdentificationData() {
	const NAME = 'identification-data' as const;

	return {
		NAME
	};
}

export function setIdentificationCtx() {
	const { NAME } = getIdentificationData();

	const identity = {
		...createIdentificationData()
	};

	setContext(NAME, identity);

	return {
		...identity
	};
}

type GetIdentityReturn = ReturnType<typeof setIdentificationCtx>;
export function getIdentityCtx() {
	const { NAME } = getIdentificationData();
	return getContext<GetIdentityReturn>(NAME);
}
