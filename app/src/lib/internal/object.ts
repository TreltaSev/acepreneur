import { Preferences } from '@capacitor/preferences';

/* eslint-disable @typescript-eslint/no-explicit-any */
export function removeUndefined<T extends object>(obj: T): T {
	const result = {} as T;
	for (const key in obj) {
		const value = obj[key];
		if (value !== undefined) {
			result[key] = value;
		}
	}
	return result;
}

/**
 * Clamps value between min and max
 * @param value
 * @param min
 * @param max
 */
export function clamp(value: number, min: number, max: number): number {
	return Math.max(min, Math.min(value, max));
}


function raise_on_no_localstorage(): void {
	if (typeof window === 'undefined')
		throw new Error("Can't access Local Storage, Window Not Applied");
}

export function clear_local(): void {
	raise_on_no_localstorage();
	localStorage.clear();
}

export function remove_local(key: string): void {
	raise_on_no_localstorage();
	localStorage.removeItem(key);
}

export function get_local(key: string): string | null {
	raise_on_no_localstorage();
	return localStorage.getItem(key);
}

export function set_local(key: string, value: any): void {
	localStorage.setItem(key, value);
}

export function has_local(key: string): boolean {
	return get_local(key) !== null;
}

export function ensureRunnable(_object?: CallableFunction) {
	if (!_object) return () => {};
	return _object;
}

export function extract_keys(data: any, ...keys: string[]): any[] {
	const extracted: any = {};
	const data_copy = { ...data };
	keys.forEach((key_to_extract) => {
		if (key_to_extract in data_copy) {
			// Save key from data to extracted
			extracted[key_to_extract] = data[key_to_extract];

			// Remove key from original data
			delete data_copy[key_to_extract];
		}
	});
	return [extracted, data_copy];
}

export function is_function(object: any): boolean {
	return typeof object === 'function';
}

export function is_valid_color(value: string): boolean {
	return /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(value);
}

/**
 * Stores a preference value using Capacitor's Preferences API.
 * The stored data persists even when the app is closed and reopened.
 *
 * @param {string} key - The key under which the preference is stored.
 * @param {string} value - The value to store for the given key.
 *
 * @returns {Promise<void>} A promise that resolves when the preference has been successfully stored.
 */
export async function set_preference(key: string, value: string): Promise<void> {
	console.debug(`Setting preference:${key} to ${value}`);
	await Preferences.set({
		key,
		value
	});
}

/**
 * Checks if a preference exists by attempting to retrieve it.
 *
 * @param {string} key - The key of the preference to check for existence.
 *
 * @returns {Promise<boolean>} A promise that resolves to `true` if the preference exists, otherwise `false`.
 */
export async function has_preference(key: string): Promise<boolean> {
	return (await get_preference(key)) !== null;
}

/**
 * Retrieves a stored preference value.
 *
 * @param {string} key - The key of the preference to retrieve.
 *
 * @returns {Promise<string | null>} A promise that resolves to the stored value for the given key, or `null` if the preference does not exist.
 */
export async function get_preference(key: string): Promise<string | null> {
	return (await Preferences.get({ key })).value;
}

/**
 * Clears all stored preferences in the app.
 *
 * @returns {Promise<void>} A promise that resolves when all preferences have been successfully cleared.
 */
export async function clear_preferences(): Promise<void> {
	return await Preferences.clear();
}

/**
 * Deletes a stored preference by key.
 *
 * @param {string} key - The key of the preference to remove.
 *
 * @returns {Promise<void>} A promise that resolves when the preference has been successfully deleted.
 */
export async function delete_preference(key: string): Promise<void> {
	return await Preferences.remove({ key });
}
