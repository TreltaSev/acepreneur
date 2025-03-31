<script lang="ts">
	import { onMount } from 'svelte';

	let { children } = $props();

	import '../app.css';

	import { setMediaCtx } from '@lib/ctx/media_size/media_size_ctx';
	import { Navigation } from '@root/lib/components';
	import { Container } from '@ui';
	import { get } from 'svelte/store';
	const { media$, set_media } = setMediaCtx(); // Set Media Ctx

	// Setup reactive media sizing
	onMount(() => {
		const callback = () => set_media();
		window.addEventListener('resize', callback);
		callback(); // Run Once

		media$.subscribe((v) => {
			if (typeof document !== 'undefined') {
				console.log('Changing');
				document.documentElement.className = ''; // Clear Document ClassName
				document.documentElement.classList.toggle(`s_${v}`);
			}
		});

		return () => {
			window.removeEventListener('resize', callback);
		};
	});

	// Apply the class on subscription update
	// mode$.subscribe((v) => {
	// 	if (typeof document !== 'undefined') {
	// 		document.documentElement.classList.toggle('dark', v === 'dark');
	// 	}
	// });
</script>

<div class="white size-full flex flex-col">
	{@render children?.()}

	<Navigation.Root />
</div>

<style>
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>
