<script lang="ts">
	import { onMount } from 'svelte';

	let { children } = $props();

	import '../app.css';

	import { setMediaCtx } from '@lib/ctx/media_size/media_size_ctx';
	import { Navigation } from '@root/lib/components';
	import { Container } from "@ui"
	import { get } from 'svelte/store';
	const { media$, set_media } = setMediaCtx(); // Set Media Ctx


	// Setup reactive media sizing
	onMount(() => {
		const callback = () => set_media();
		window.addEventListener('resize', callback);
		callback(); // Run Once

		console.log("mounting", get(media$))

		media$.subscribe((v) => {
			console.log(v, "change")
			if (typeof document !== 'undefined') {
				console.log("Changing")
				document.documentElement.className = ''; // Clear Document ClassName
				document.documentElement.classList.toggle(`s_${v}`);
			}

			console.log(document.documentElement.className)
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

	<Container class="size-50 s_2xl:bg-red-500 s_xl:bg-blue-500 s_lg:bg-green-500 s_md:bg-amber-400 s_sm:bg-fuchsia-500 s_xs:bg-amber-950 s_xs:border-indigo-700 fixed left-0 top-0 transform translate-x-1/2 translate-y-1/2">
	
	<span>y u no show?</span>
	</Container>

	<Navigation.Root>

	</Navigation.Root>
</div>

<style>
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>
