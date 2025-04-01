<script lang="ts">
	import '../app.css';

	// --- Components ---
	import { Flex } from '@ui';
	import { Navigation } from '@components';

	// --- Logic ---
	import { setPlatformCtx, setMediaCtx } from '@root/lib/ctx';
	import { onMount } from 'svelte';
	import { SafeArea } from '@capacitor-community/safe-area';

	let { children } = $props();

	const { media$, set_media } = setMediaCtx(); // Set Media Ctx
	const { platform$ } = setPlatformCtx();

	function remove_variant(start: string) {
		document.documentElement.classList.forEach((cls) => {
			if (cls.startsWith(start)) {
				document.documentElement.classList.remove(cls);
			}
		});
	}

	SafeArea.enable({
		config: {
			customColorsForSystemBars: true,
			statusBarColor: '#00000000', // transparent
			statusBarContent: 'dark',
			navigationBarColor: '#00000000', // transparent
			navigationBarContent: 'dark'
		}
	});

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
</script>

<div class="white size-full flex flex-col items-center">
	<Flex.Col class="size-full s_2xl:w-[50%] pt-[var(--safe-area-inset-top)]">
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
