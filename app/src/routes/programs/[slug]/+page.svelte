<script lang="ts">
	// --- Components ---
	import { Flex } from '@root/lib/ui';

	// --- Logic ---
	import { onMount } from 'svelte';
	import { getColorCtx, getIdentityCtx } from '@root/lib/ctx';
	import { State } from '@internal/state.svelte';
	import type { Program, Event } from '@internal/types';
	import { cn } from '@root/lib/utils';

	// Slug data object
	import { page } from '$app/state';
	const slug = page.params.slug;

	// Gather user object from the identity context
	const { user } = getIdentityCtx();

	// Get Color Context
	const { color$ } = getColorCtx();

	// Reactive State to store program information
	let program: Program | undefined = $state(undefined);
	let load_state = $state(new State());
	let events: Event[] = $state([]); // Store loaded events

	// Fetch the specified program on load
	onMount(async () => {
		const fetched_program = await user.get_program(slug);

		if (!fetched_program) {
			load_state.flagError();
			return;
		}

		program = fetched_program;
		color$.set(program.card.color);
		load_state.flagLoaded();

		// Load event data
		for (const event of program.events) {
			const _event_data = await user.get_event(event);
			if (_event_data) {
				events.push(_event_data);
			}
		}
	});
</script>

{#if load_state.value == 'loading'}
	<span>Loading</span>
{/if}

{#if load_state.value == 'error'}
	<span>Error</span>
{/if}

{#if load_state.value == 'loaded' && program}
	<Flex.Col class="gap-8 blueprint-content-container relative pb-16">
		<Flex.Col class="gap-8">
			<!-- Program Image-->
			<img
				src={program.card.image.url}
				alt={`background of ${program.name}`}
				class={cn('w-full rounded-3xl aspect-2/1 object-cover', program.card.image._class)}
				style={program.card.image.style}
			/>

			<!-- Program Name and Description -->
			<Flex.Col>
				<h3>{program.name}</h3>
				<h4>{program.description}</h4>
			</Flex.Col>

			<!-- Announcement Goes Here -->
		</Flex.Col>

		<!-- Page Content Goes Here -->
		<Flex.Col class="pb-8">
			{@html program?.content.blueprint}
		</Flex.Col>

		<!-- Events Section -->
		{#if events.length > 0}
			<Flex.Col class="gap-8">
				<h2 class="">Events</h2>
				{#each events as event, index}
					<Flex.Col class="p-4 rounded-2xl gap-12">
						<Flex.Row class="items-center justify-center gap-8">
							<h3
								class="text-3xl text-black overflow-hidden text-ellipsis whitespace-nowrap w-full"
							>
								{event.name}
							</h3>
							<a href={`/events/${event.slug}`} class="px-4 py-2 text-white bg-app rounded-lg">
								<h4 class="text-white whitespace-nowrap">View Event</h4>
							</a>
						</Flex.Row>
						<h4>{event.description}</h4>
						<div>{@html event.content.blueprint}</div>
						{#if index < events.length - 1}
							<hr class="border-black/20" />
						{/if}
					</Flex.Col>
				{/each}
			</Flex.Col>
		{/if}
	</Flex.Col>
{/if}

<style>
	:global(.blueprint-content-container) {
		& h4 {
			opacity: 60%;
		}

		& button {
			@apply w-full;
			padding-top: calc(var(--spacing) * 4);
			padding-bottom: calc(var(--spacing) * 4);
			color: white;
			font-size: large;
			border-radius: calc(var(--spacing) * 4);
			background-color: var(--color-app);
			margin-top: calc(var(--spacing) * 4);
		}
	}

	:global(.event-card) {
		background-color: var(--color-background);
		border: 1px solid var(--color-border);
	}
</style>
