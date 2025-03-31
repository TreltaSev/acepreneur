<script lang="ts">
	import { onMount } from 'svelte';

	let { children } = $props();

	import '../app.css';

	import { setMediaCtx } from '@lib/ctx/media_size/media_size_ctx';
	const { media$, set_media } = setMediaCtx(); // Set Media Ctx


	// Setup reactive media sizing
	onMount(() => {
		const callback = () => set_media();
		window.addEventListener('resize', callback);
		callback(); // Run Once

		media$.subscribe((v) => {
			if (typeof document !== 'undefined') {
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

<div class="white size-full">
	{@render children?.()}
</div>

<style>
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>
