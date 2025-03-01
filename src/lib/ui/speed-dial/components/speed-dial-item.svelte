<script lang="ts">
	import { cn } from '@lib/utils';
	import type { ItemProps } from '..';

    import { Flex } from "@ui"
	import { type Props as tFlexProps } from '@ui/flex';
	import { getCtx } from '../ctx';
	import { onDestroy, onMount } from 'svelte';

 	// -=-=-=-=- Static Classes -=-=-=-=- //
    const ITEM_CLASS = "hover:bg-stone-100 bg-gray-300 shrink-0 transition-all ease-in cursor-pointer w-10 h-10 rounded-full items-center justify-center"

	// -=-=-=-=- Props -=-=-=-=- //
	type $$Props = ItemProps & tFlexProps;
	let className: $$Props['class'] = undefined;
	export let el: $$Props['el'] = undefined;	
	export { className as class }

</script>

<Flex.Col class={cn(ITEM_CLASS, className)} {...$$restProps} on:click>
	<slot />
</Flex.Col>
