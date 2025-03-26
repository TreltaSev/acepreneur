
/**
 * Adds the events below
 * 
 * ### outclick
 * Fires when click outside of node
 * #### Usage
 * ```
 * <element use:directives on:outclick={}/>
 * ```
 * @param node 
 * @returns 
 */
export function directives(node: Node) {
	const handleClick = (event: MouseEvent) => {
		if (!node.contains(event.target as Node)) {
			node.dispatchEvent(new CustomEvent('outclick'));
		}
	};

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	};
}