<script lang="ts">
	import { State } from '@root/lib/internal';
	import { isAndroid, isIOS } from 'mobile-device-detect';
	import { onMount } from 'svelte';

	let onAndroid = $state(false);
	let oniOS = $state(false);
    let load_state = $state(new State())

	onMount(() => {
		onAndroid = isAndroid;
		oniOS = isIOS;
        load_state.flagLoaded()
	});

</script>

{#if load_state.value == "loading"}
    <span>Loading...</span>
{/if}

{#if load_state.value == "loaded"}

    {#if onAndroid}
        <span>The easy lane, heres a download link:</span>
    {:else if oniOS}
        <span>Heres the tricky part. click this button, we'll ask you for some perms</span>
    {:else}
        <span>You're on a computer... THERES NOTHING TO INSTALL!!!</span>
    {/if}
{/if}
