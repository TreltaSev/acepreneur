<script lang="ts">
	// Global CSS import
	import '../app.css';

	// --- UI Components ---
	import { Flex } from '@ui';
	import { Navigation } from '@components';

	// --- Context setup functions for shared app state ---
	import { setPlatformCtx, setMediaCtx, setIdentificationCtx, setColorCtx } from '@root/lib/ctx';

	// Svelte lifecycle
	import { onMount } from 'svelte';

	// Native device functionality via Capacitor
	import { SafeArea } from '@capacitor-community/safe-area';
	import { ScreenOrientation } from '@capacitor/screen-orientation';
	import { App } from '@capacitor/app';
	import { afterNavigate } from '$app/navigation';
	import { Capacitor } from '@capacitor/core';

	// `children` will be rendered as a slot from routes using this layout
	let { children } = $props();

	// Setup shared contexts and extract key reactive stores
	const { media$, set_media } = setMediaCtx();
	const { platform$ } = setPlatformCtx();
	const { user } = setIdentificationCtx();
	const { color$ } = setColorCtx(); // Initialize global color context

	// Store current location string (updated after navigation)
	let location = $state('Hi there');

	/**
	 * Utility function to remove all document class names that start with a given prefix.
	 * This is used to clear media (`s_`) or platform (`p_`) variants before applying new ones.
	 * @param start Prefix string to match class names against.
	 */
	function remove_variant(start: string) {
		document.documentElement.classList.forEach((cls) => {
			if (cls.startsWith(start)) {
				document.documentElement.classList.remove(cls);
			}
		});
	}

	// Enable transparent system bars and dark content for status/navigation
	SafeArea.enable({
		config: {
			customColorsForSystemBars: true,
			statusBarColor: '#00000000',
			statusBarContent: 'dark',
			navigationBarColor: '#00000000',
			navigationBarContent: 'dark'
		}
	});

	/* Only run native-specific logic in the browser context */
	if (typeof window !== 'undefined') {
		if (Capacitor.isNativePlatform()) {
			// Lock screen orientation to portrait on native devices
			try {
				ScreenOrientation.lock({ orientation: 'portrait' });
			} catch (error) {
				console.warn(`[screen-orientation] Browser does not support the screen orientation api.`);
			}
		} else {
		}
	}

	// Setup logic to run once the component is mounted
	onMount(() => {
		user.request_identity(); // Trigger identity detection (e.g., login state)

		// Recalculate media size when the window resizes
		const callback = () => set_media();
		window.addEventListener('resize', callback);
		callback(); // Run once initially

		if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
			navigator.serviceWorker.register('/service-worker.js');
		}

		// Dynamically update media class on document
		media$.subscribe((v) => {
			if (typeof document !== 'undefined') {
				remove_variant('s_');
				document.documentElement.classList.toggle(`s_${v}`);
			}
		});

		// Dynamically update platform class on document
		platform$.subscribe((v) => {
			if (typeof document !== 'undefined') {
				remove_variant('p_');
				document.documentElement.classList.toggle(`p_${v}`);
			}
		});

		// Listen for native back button events (Android)
		App.addListener('backButton', () => {
			if (window.location.pathname == '/events') {
				App.exitApp(); // Exit app from /events route
				return;
			}
			window.history.back(); // Otherwise go back
		});

		// Keep --app-color reactive
		color$.subscribe((color) => {
			const fallback = getComputedStyle(document.documentElement)
				.getPropertyValue('--color-primary')
				?.trim();
			document.documentElement.style.setProperty('--color-app', color ?? fallback);
		});

		// Cleanup resize listener on unmount
		return () => {
			window.removeEventListener('resize', callback);
		};
	});

	// Update internal location state when navigating pages
	afterNavigate(() => {
		location = window.location as unknown as string;
		color$.set(null);
	});
</script>

<svelte:head>
	<link rel="manifest" href="/manifest.webmanifest" />
	<meta name="theme-color" content="#0084ff" />
	<meta name="mobile-web-app-capable" content="yes" />
	<meta name="apple-mobile-web-app-capable" content="yes" />
	<link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
	<meta name="apple-mobile-web-app-status-bar-style" content="default" />
	<link rel="apple-touch-icon" href="/icons/icon-192.png" />
</svelte:head>

<!-- App container with full height and white background -->
<div class="white size-full flex flex-col items-center">
	<!-- Content column with responsive width and padding based on media and platform -->
	<Flex.Col
		class="size-full s_2xl:w-[50%] px-10 pt-[calc(var(--safe-area-inset-top)_+_1rem)] p_ios:pt-30 p_web:pt-10 overflow-y-auto"
	>
		<!-- Render child route content -->
		{@render children?.()}
	</Flex.Col>

	<!-- Persistent navigation bar at the bottom -->
	<Navigation.Root />
</div>

<style>
	/* Ensure root HTML and body fill the entire viewport */
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>
