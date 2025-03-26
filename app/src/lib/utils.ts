import { clsx, type ClassValue } from 'clsx';
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
