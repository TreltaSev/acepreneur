/* eslint-disable @typescript-eslint/no-explicit-any */
import { base } from '$app/paths';
import { clsx, type ClassValue } from 'clsx';
import { cubicOut } from 'svelte/easing';
import { twMerge } from 'tailwind-merge';

/**
 * Fix class naming conflicts by utilizing both :function:`twMerge` and :function:`clsx`
 * clsx allows very precise boolean specific class loading and twMerge removes all the conflicting but unused classes.
 * @param inputs All base classes
 * @returns Merged classes
 */
export function cn(...inputs: (ClassValue | unknown)[]) {
	return twMerge(clsx(inputs));
}

/**
 * Allows for easy creation of data attribute specific classes in tailwind.
 * First, you create the builder while specifying the root selector. then you can call
 * `cn_a.build('bg-black')`.
 *
 * ## Usage
 * ```ts
 * const builder = new cn_a("state=toggled")
 * builder.build("bg-black text-white") // >> "data-[state=toggled]:bg-black data-[state=toggled]:text-white"
 *
 * // Or
 * cn_a.buildx("state=toggled", "bg-black text-white") // >> "data-[state=toggled]:bg-black data-[state=toggled]:text-white"
 *
 * ```
 */
export class cn_a {
	public selector: string | undefined;

	constructor(selector: string) {
		this.selector = selector;
	}

	/**
	 * Returns a string of all the classes with the attribute selector attached
	 * @param {string} classes tailwind/css classes string
	 * @returns
	 */
	build(classes: string) {
		// Make sure to stop if selector is not specified
		if (!this.selector) {
			console.warn(
				'[classname_attribute_builder] Failed to build: Selector Undefined, Tried to build:',
				classes
			);
			return '';
		}

		// Convert a class string such as "bg-black flex flex-col" into ["bg-black", "flex", "flex-col"]
		const classes_indexed: string[] = classes.split(' ');

		const buffer: string[] = [];

		classes_indexed.forEach((_class: string) => {
			buffer.push(`${cn_a.wrap_selector(this.selector || '')}:${_class}`); // Join selector and class
		});

		return buffer.join(' '); // Return all the changes split
	}

	/**
	 *
	 * @param selector some sort of boolean expression like state=toggled...
	 * @returns `data-[${selector}]`
	 */
	public static wrap_selector(selector: string) {
		return `data-[${selector}]`;
	}

	/**
	 *
	 * @param selector data attribute selector like state=toggled
	 * @param classes
	 */
	public static buildx(selector: string, classes: string) {
		// Convert a class string such as "bg-black flex flex-col" into ["bg-black", "flex", "flex-col"]
		const classes_indexed: string[] = classes.split(' ');

		const buffer: string[] = [];

		classes_indexed.forEach((_class: string) => {
			buffer.push(`${cn_a.wrap_selector(selector || '')}:${_class}`); // Join selector and class
		});

		return buffer.join(' '); // Return all the changes split
	}
}

export function expand(node: HTMLElement, params: any, { duration = 300}) {
	const height = node.scrollHeight;

	return {
		duration,
		easing: params.easing || cubicOut,
		css: (t: number) => `height: ${t * height}px; opacity: ${t}; margin-top: ${t * ((params.offset !== undefined) ? params.offset : 8)}px;`
	};
}

export function uuidv4() {
	return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, (c) =>
		(+c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+c / 4)))).toString(16)
	);
}

export function reference_package_to_form(package_name: string, location: string | undefined = undefined) {
	let buff: string = `?tour-package=${package_name}`;
	if (location !== undefined) {
		buff += `&location=${location}`
	}
	window.location.href=`${base}/form${buff}`
	return buff
}
