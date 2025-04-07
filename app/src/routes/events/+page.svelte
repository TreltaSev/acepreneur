<script lang="ts">

    // --- Components ---
	import { EventCard } from './_components';

    // --- Logic ---
	import { getIdentityCtx } from '@root/lib/ctx';
	import type { Event } from '@internal/types';
	import { onMount } from 'svelte';

    // Gathering user object from the identity context
	const { user } = getIdentityCtx();

    // Reactive States to handle what should be rendered
	let cached_events: Event[] = $state([]);
	let loaded: boolean = $state(false);

    // Fetch the events on load
	onMount(async () => {
		const events = await user.get_events();
		cached_events = events; // Save Events
        loaded = true; // Stop "Loading"
	});

</script>

<h1>Events</h1>

{#if !loaded}
	<!-- Loading -->
	<span>We are fetching the events for you!</span>
{/if}

{#if loaded}
	{#if cached_events.length == 0}
		<!-- No Events, Display some error message -->
		<span>No events found, try again later :)</span>
	{:else}
		<!-- Events found, display events-->
		<span>Events found</span>

		{#each cached_events as event}
			<EventCard data={event}/>
		{/each}
	{/if}
{/if}
