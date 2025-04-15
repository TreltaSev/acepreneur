<script lang="ts">
	// --- Components ---
	import { EventCard } from './_components';

	// --- Logic ---
	import { getIdentityCtx } from '@root/lib/ctx';
	import type { Event } from '@internal/types';
	import { onMount } from 'svelte';
	import { Flex } from '@root/lib/ui';

	// Gathering user object from the identity context
	const { user } = getIdentityCtx();

	// Reactive States to handle what should be rendered
	let cached_events: Event[] = $state([]);
	let loaded: boolean = $state(false);

	// Fetch the events on load
	onMount(async () => {
		const events = await user.get_events();
		cached_events = events; // Save Events

		cached_events = cached_events.sort((a, b) => {
			return  a.name.localeCompare(b.name)
		})

		cached_events = cached_events.sort((a, b) => {
				return (
					Number(a.order ?? 10) -
					Number(b.order ?? 10)
				);
			});
		loaded = true; // Stop "Loading"
	});
</script>

<img src="https://res.cloudinary.com/dtuexxqi2/image/upload/v1744469396/large_7f6bfcb0-9485-4cf6-807c-95cb3c07e087-removebg-preview_yeayq3.png" alt="Card" class="w-full object-cover aspect-2/1 border-2xl"/>
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
		<Flex.Col class="gap-20 mt-10 mb-20 pb-20">
			{#each cached_events as event}
				<EventCard data={event} />
			{/each}
		</Flex.Col>
	{/if}
{/if}
