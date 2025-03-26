<script lang="ts">
	import { cn } from '@lib/utils';
	import type { MenuProps } from '..';
	import { portal } from 'svelte-portal';

	import { setCtx } from '../ctx';
	import type { ClassValue } from 'clsx';
	import { getContext, setContext } from 'svelte';
	import { type ToggleableWritable } from '@lib/internal';
	import { directives } from '@lib/internal/directives';

	// -=-=-=-=- Get Contexts -=-=-=-=- //
	let parentActive$: ToggleableWritable | undefined = getContext('parentActive$');

	// -=-=-=-=- Props -=-=-=-=- //
	type $$Props = MenuProps;
	export let className: $$Props['class'] = undefined;
	export let anchorClass: $$Props['anchorClass'] = undefined;
	export let direction: $$Props['direction'] = 'left';
	export let anchor: $$Props['anchor'] = '';
	export let parent: boolean | undefined = undefined;
	let menu: HTMLDivElement;

	export { className as class };

	export let { isActive$ } = setCtx();

	const menu_class: ClassValue[] = [
		'flex bottom-0 transition-all ease-in-out duration-500 box-border',
		direction == 'up' && 'flex-col bottom-full py-5',
		direction == 'right' && 'flex-row left-full px-5',
		direction == 'down' && 'flex-col top-full py-5',
		direction == 'left' && 'flex-row right-full px-5'
	];

	// Close all children menus
	if (parent) {
		parentActive$ = isActive$;
		setContext('parentActive$', parentActive$);
	} else {
		parentActive$?.subscribe((v) => {
			if (!v) {
				isActive$.set(v);
			}
		});
	}

	function onoutclick(event: CustomEvent) {
		if ($parentActive$) {
			parentActive$?.toggle(false);
		}
	}
</script>

<div bind:this={anchor} class={cn('relative', anchorClass)}>
	<button bind:this={anchor} class="relative z-1" on:click={() => isActive$.toggle()}>
		<slot name="anchor" />
	</button>
</div>

<div
	bind:this={menu}
	use:portal={anchor}
	use:directives
	on:outclick={onoutclick}
	class={cn(
		'w-fit h-fit absolute z-0',
		...menu_class,
		$isActive$ && `visible p${['left', 'right'].includes(direction || '') ? 'x' : 'y'}-5 gap-2.5`,
		!$isActive$ &&
			`opacity-0 p${['left', 'right'].includes(direction || '') ? 'x' : 'y'}-1 gap-0 invisible`,
		className
	)}
>
	<slot />
</div>
