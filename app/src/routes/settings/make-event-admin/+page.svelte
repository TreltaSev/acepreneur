<script lang="ts">
	// --- Components ---
	import { AdminOnly } from '@components';
	import { getIdentityCtx } from '@root/lib/ctx';

	// --- Logic ---
	const { user } = getIdentityCtx();
	import { State } from '@internal';
	import { onMount } from 'svelte';
	import type { Event } from '@internal/types';
	import { Flex } from '@root/lib/ui';

	// Reactive state to store events
	let events: Event[] = $state([]);
	let load_state = $state(new State());

	// Fetch all events
	onMount(async () => {
		events = (await user.get_events()).sort((a, b) => {
			return Number(a.order ?? Infinity) - Number(b.order ?? Infinity);
		});

		load_state.flagLoaded();
	});

	function gen_qr_for(event_id: string) {
		console.log('gen', event_id);
	}
</script>

<AdminOnly class="flex flex-col gap-5">
	<h1>Making Admin</h1>
	<h2 class="mb-10">Choose Event</h2>

	{#if load_state.value == 'loading'}
		<span>Loading...</span>
	{/if}

	{#if load_state.value == 'error'}
		<span>Failed to load...?</span>
	{/if}

	{#if load_state.value == 'loaded'}
		<span>Loaded!</span>

		{#if events.length == 0}
			<span>Hmm, there aren't any events</span>
		{/if}

		{#if events.length > 0}
			<Flex.Col class="gap-10">
				{#each events as event}
					<a href={`/settings/make-event-admin/${event.slug}`}>
						<Flex.Row
							class="py-4 pl-10 box-border border-b border-black/40 bg-black/5 rounded-2xl overflow-hidden"
							onclick={() => {
								gen_qr_for(event.slug);
							}}
						>
							<h3>{event.name}</h3>
						</Flex.Row>
					</a>
				{/each}
			</Flex.Col>
		{/if}
	{/if}
</AdminOnly>
