<script lang="ts">
	import { Button } from '@components';
	import { State } from '@root/lib/internal';
	import { Flex } from '@root/lib/ui';
	import { isAndroid, isIOS } from 'mobile-device-detect';
	import { onMount } from 'svelte';

	let onAndroid = $state(false);
	let oniOS = $state(false);
	let load_state = $state(new State());

	import IconAndroid from '~icons/icon-park-solid/android';

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
				class="text-[#a4c639] color-red-400"
				mode="outline"
				text="Download APK"
				onclick={download}><IconAndroid /></Button
			>

			<h3>Or you could use this website instead of the app (Not recommended)</h3>
		</Flex.Col>
	{:else if oniOS}
		<h1>Hi there...</h1>
		<h2>If you're seeing this, that means the app wasn't reviewed on time :(</h2>
		<h4>
			This means that on iphone, this isn't an official app. so you could just use this website as
			the app.
		</h4>
	{:else}
		<span>You're on a computer... THERES NOTHING TO INSTALL!!!</span>
	{/if}
{/if}
