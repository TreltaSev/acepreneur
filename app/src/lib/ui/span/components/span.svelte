<script lang="ts">
	import { cn } from '@lib/utils';
	import type { Props } from '..';

	// -=-=-=-=- Props -=-=-=-=- //
	type $$Props = Props;

	let className: $$Props['class'] = undefined;
	export { className as class };

	export let spanClass = 'text-black dark:text-white';

	$: spanCls = cn(spanClass, className);
</script>

<span class={cn(spanCls)} {...$$restProps} on:click>
	<slot />
</span>
