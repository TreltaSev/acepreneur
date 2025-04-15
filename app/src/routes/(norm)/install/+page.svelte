<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '@components';
	import { State } from '@root/lib/internal';
	import { Flex } from '@root/lib/ui';
	import { isAndroid, isIOS } from 'mobile-device-detect';
	import { onMount } from 'svelte';

	let onAndroid = $state(false);
	let oniOS = $state(false);
	let load_state = $state(new State());

	import IconAndroid from '~icons/icon-park-solid/android';
	import IconAppStore from '~icons/mingcute/appstore-fill';

	onMount(() => {
		console.log(isAndroid, isIOS);
		onAndroid = isAndroid;
		oniOS = isIOS;
		load_state.flagLoaded();
	});

	function download() {
		const link = document.createElement('a');
		link.href = 'https://github.com/TreltaSev/acepreneur/releases/latest/download/acepreneur.apk';
		link.download = 'acepreneur.apk'; // not required, but helps suggest filename
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	function iosDownload() {
		window.location.href = "https://apps.apple.com/app/6744039406"
	}
</script>

{#if load_state.value == 'loading'}
	<span>Loading...</span>
{/if}

{#if load_state.value == 'loaded'}
	{#if onAndroid}
		<Flex.Col class="gap-4">
			<h2>Hi there, You have two choices.</h2>
			<h3>You can either hit the download button below, and install the app.</h3>
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
