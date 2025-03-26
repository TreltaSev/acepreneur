<script lang="ts">
	import { cn } from '@lib/utils';
	import type { Props } from '..';

	import { Flex } from '@ui';

	// -=-=-=-=- Props -=-=-=-=- //
	let {
		children,
		class: className,
		pageClass = 'flex flex-col size-full items-center justify-center select-none z-2 box-border'
	}: Props & any = $props();

	let pageCls = $state("")

	$effect(() => {
		pageCls = cn(pageClass, className);
	})

</script>

<Flex.Col class={pageCls}>
	{@render children?.()}
</Flex.Col>
