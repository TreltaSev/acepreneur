<script lang="ts">
	import { State } from '@root/lib/internal';
	import { isAndroid, isIOS } from 'mobile-device-detect';
	import { onMount } from 'svelte';

	let onAndroid = $state(false);
	let oniOS = $state(false);
	let load_state = $state(new State());

	onMount(() => {
		onAndroid = isAndroid;
		oniOS = isIOS;
		load_state.flagLoaded();
	});

	$effect(() => {
		if (onAndroid) {
			const link = document.createElement('a');
			link.href = 'https://github.com/TreltaSev/acepreneur/releases/latest/download/acepreneur.apk';
			link.download = 'acepreneur.apk'; // not required, but helps suggest filename
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		}
	});
</script>

{#if load_state.value == 'loading'}
	<span>Loading...</span>
{/if}

{#if load_state.value == 'loaded'}
	{#if onAndroid}
        <h2>We're downloading the app for you</h2>
        <h3>After it's been downloaded, install it on your device :)</h3>
	{:else if oniOS}
		<h1>Hi there...</h1>
        <h2>If you're seeing this, that means the app wasn't reviewed on time :(</h2>
        <h3>What does this mean?</h3>
        <p>Well, in short. It means this app on IOS is severely more restricted and more annoying to setup then if you were on an android device</p>
        <h3>What can I do?</h3>
        <p>You can still continue to use this app, but not the way it was intended.</p>

        <!-- Check if on safari -->
        <h4>At this point, I recommend you use Safari, it looks like you aren't using it right now</h4>
        <p>You should be prompted to add this device to your home-screen.</p>

	{:else}
		<span>You're on a computer... THERES NOTHING TO INSTALL!!!</span>
	{/if}
{/if}
