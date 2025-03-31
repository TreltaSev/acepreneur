<script lang="ts">
	import { onMount } from 'svelte';

	let { children } = $props();

	import '../app.css';

	import { Navigation } from '@root/lib/components';
	import { Container, Flex } from '@ui';
	import { get } from 'svelte/store';
	import { Capacitor } from '@capacitor/core';
	import { setPlatformCtx, setMediaCtx } from '@root/lib/ctx';

	const { media$, set_media } = setMediaCtx(); // Set Media Ctx
	const { platform$ } = setPlatformCtx();

	function remove_variant(start: string) {
		document.documentElement.classList.forEach((cls) => {
			if (cls.startsWith(start)) {
				document.documentElement.classList.remove(cls);
			}
		});
	}

	// Setup reactive media sizing
	onMount(() => {
		const callback = () => set_media();
		window.addEventListener('resize', callback);
		callback(); // Run Once

		media$.subscribe((v) => {
			if (typeof document !== 'undefined') {
				remove_variant('s_'); // Remove Media Sizing Document ClassName
				document.documentElement.classList.toggle(`s_${v}`);
			}
		});

		platform$.subscribe((v) => {
			if (typeof document !== 'undefined') {
				remove_variant('p_'); // Remove Platform Document ClassName
				document.documentElement.classList.toggle(`p_${v}`);
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

<div class="white size-full flex flex-col items-center">
	<Flex.Col class="size-full s_2xl:w-[50%] p_ios:pt-12 p_android:pt-4">
		{@render children?.()}
	</Flex.Col>

	<Navigation.Root />
</div>

<style>
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>
