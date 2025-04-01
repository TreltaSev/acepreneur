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
	return typeof object === "function"
}

export function is_valid_color(value: string): boolean {
	return /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(value);
}