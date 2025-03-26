<script lang="ts">
	import { cn } from '@lib/utils';
	import type { Props } from '..';

	// -=-=-=-=- Props -=-=-=-=- //
	type $$Props = Props;

	export let href: $$Props['href']= undefined;
	export let newPage: $$Props['newPage']= undefined;

	let className: $$Props['class'] = undefined;
	export { className as class };

	export let buttonClass =
		'flex flex-col p-[10px] px-[20px] justify-center items-center bg-primary-500 rounded-[10px] cursor-pointer overlay h-fit text-white dark:text-white';
	

	$: buttonCls = cn(buttonClass, className);
</script>

{#if href}
	<a {href} class={buttonCls} target={newPage ? "_blank" : "_self"}>
		<button {...$$restProps} on:click>
			<slot />
		</button>
	</a>
{:else}
	<button class={buttonCls} {...$$restProps} on:click>
		<slot />
	</button>
{/if}
