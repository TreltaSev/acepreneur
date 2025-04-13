/* eslint-disable @typescript-eslint/no-explicit-any */
import { getContext, setContext } from 'svelte';
import { get, writable, type Writable } from 'svelte/store';
import { User } from './user';
import { Preferences } from '@capacitor/preferences';
import { get_preference, set_preference } from '@root/lib/internal';

export function createIdentificationData() {
	const identity$: Writable<string | null> = writable(null);
	const dev_admin$: Writable<boolean | null> = writable(null);

	const user: User = new User();

	identity$.subscribe(async (current_identity) => {
		if (!current_identity) return;
		await set_preference('identity', current_identity);
	});

	setInterval(async () => {
		if (typeof window === 'undefined' || !Preferences) return;
		try {
			const userIdentity = await get_preference('identity');
			if (get(identity$) != userIdentity) {
				identity$.set(userIdentity);
			}

			if ((await get_preference('dev-admin')) === null) {
				return;
			}

			const dev_admin = (await get_preference('dev-admin')) === 'true' ? true : false;
			if (get(dev_admin$) != dev_admin) {
				dev_admin$.set(dev_admin);
			}
		} catch (error) {
			console.warn(`Error`, error);
			return;
		}
	}, 50);

	return {
		identity$,
		dev_admin$,
		user
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
