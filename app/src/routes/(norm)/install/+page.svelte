<script lang="ts">
	import { Button } from '@components';
	import { State } from '@internal';
	import { Flex } from '@ui';
	import { isAndroid, isIOS } from 'mobile-device-detect'; // Detect mobile platforms
	import { onMount } from 'svelte'; // Lifecycle hook for component initialization

	// Import icons for Android and iOS
	import IconAndroid from '~icons/icon-park-solid/android';
	import IconAppStore from '~icons/mingcute/appstore-fill';

	// Reactive state variables
	let onAndroid = $state(false); // Tracks if the device is Android
	let oniOS = $state(false); // Tracks if the device is iOS
	let load_state = $state(new State()); // Tracks the loading state of the page

	// Lifecycle hook to detect platform and update state
	onMount(() => {
		onAndroid = isAndroid;
		oniOS = isIOS;
		load_state.flagLoaded(); // Mark the state as loaded
	});

	// Function to download the Android APK
	function download() {
		const link = document.createElement('a');
		link.href = 'https://github.com/TreltaSev/acepreneur/releases/latest/download/acepreneur.apk';
		link.download = 'acepreneur.apk'; // Suggests filename for download
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	// Function to redirect to the iOS App Store
	function iosDownload() {
		window.location.href = "https://apps.apple.com/app/6744039406";
	}
</script>

<!-- Conditional rendering based on loading state and platform -->
{#if load_state.value == 'loading'}
	<span>Loading...</span>
{/if}

{#if load_state.value == 'loaded'}
	{#if onAndroid}
		<Flex.Col class="gap-4">
			<h2>Hi there, You have two choices.</h2>
			<h3>You can either hit the download button below, wait for it to download, you'll be then prompted to install the app.</h3>
			<h4>You might need to allow your browser to install apps from unknown sources</h4>
			<h4>On most phones, on that prompt, hit settings and click your browser. It will then ask you again to install the app.</h4>
			<h4>If it asks you to scan the app, just scan it. It might take a minute.</h4>
			<Button
				class="text-[#a4c639]"
				mode="outline"
				text="Download APK"
				onclick={download}><IconAndroid /></Button
			>

			<h3>Or you could use this website instead of the app (Not recommended)</h3>
		</Flex.Col>
	{:else if oniOS}
		<Flex.Col class="gap-4">
			<h2>Hi there, You have two choices.</h2>
			<h3>You can either install the app on the app-store by clicking the button below.</h3>
			<Button
				class="text-black"
				mode="outline"
				text="Visit the App Store"
				onclick={iosDownload}><IconAppStore /></Button
			>

			<h3>Or you could use this website instead of the app (Not recommended)</h3>
		</Flex.Col>
	{:else}
		<h2>It seems like you're on a computer...</h2>
		<h3>If you aren't, welp that sucks. Stop messing with your user-agent?</h3>
	{/if}
{/if}
