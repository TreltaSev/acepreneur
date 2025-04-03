<script lang="ts">
	import '../app.css';

	// --- Components ---
	import { Flex } from '@ui';
	import { Navigation } from '@components';

	// --- Logic ---
	import { setPlatformCtx, setMediaCtx, setIdentificationCtx } from '@root/lib/ctx';
	import { onMount } from 'svelte';
	import { SafeArea } from '@capacitor-community/safe-area';
	import { App } from '@capacitor/app';
	import { afterNavigate } from '$app/navigation';
	import Container from '@root/lib/ui/container/components/container.svelte';

	let { children } = $props();

	const { media$, set_media } = setMediaCtx(); // Set Media Ctx
	const { platform$ } = setPlatformCtx();
	const { user } = setIdentificationCtx();
	let location = $state('Hi there');

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
		user.request_identity();
		// --- Context APIS --- //
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

		// --- Capacitor Native Listeners --- //

		// Back Arrow
		App.addListener('backButton', () => {
			if (window.location.pathname == '/events') {
				App.exitApp();
				return;
			}
			window.history.back();
		});

		return () => {
			window.removeEventListener('resize', callback);
		};
	});

	/* Testing Requests */
	onMount(async () => {
		// user.get_events()
	});

	afterNavigate(() => {
		location = window.location as unknown as string;
	});

	const apiUrl = import.meta.env.VITE_API_URL;
</script>

<div class="white size-full flex flex-col items-center">
	<Flex.Col class="size-full s_2xl:w-[50%] pt-[var(--safe-area-inset-top)] overflow-y-auto">
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
