<script lang="ts">
	// --- Components ---
	import { Flex } from '@root/lib/ui';
	import { Edit } from './_components';
	import {ProgramLink} from './_components';
	import IconAnnounce from '~icons/mingcute/announcement-fill';


	// --- Logic ---
	import { onMount } from 'svelte';
	import { getColorCtx, getIdentityCtx } from '@root/lib/ctx';
	import { State } from '@internal/state.svelte';
	import type { Event } from '@internal/types';
	import { cn } from '@root/lib/utils';

	// Slug data object
	import { page } from '$app/state';
	const slug = page.params.slug;

	// Gather user object from the identity context
	const { user,  identity$} = getIdentityCtx();

    // Get Color Context
	const { color$ } = getColorCtx();


	// Reactive State to store event information
	let event: Event | undefined = $state(undefined);
	let load_state = $state(new State());

	let asAdmin: boolean = $state(false);

	// Fetch the specified event on load
	onMount(async () => {
		const fetched_event = await user.get_event(slug);

		if (!fetched_event) {
			load_state.flagError();
			return;
		}

		event = fetched_event;
        color$.set(event.card.color)
		asAdmin = (event as any).asAdmin as boolean
		load_state.flagLoaded();
		console.log(event)
	});
</script>

{#if load_state.value == 'loading'}
	<span>Loading</span>
{/if}

{#if load_state.value == 'error'}
	<span>Error</span>
{/if}

{#if load_state.value == 'loaded' && event}
	<Flex.Col class="gap-8 blueprint-content-container relative pb-16">
		<Flex.Col class="gap-8">
			<!-- Event Image-->
			<img
				src={event.card.image.url}
				alt={`background of ${event.name}`}
				class={cn('w-full rounded-3xl aspect-2/1 object-cover', event.card.image._class)}
				style={event.card.image.style}
			/>

			<!-- Event Name and Description -->
			<Flex.Col>
				<h3>{event.name}</h3>
				<h4>{event.description}</h4>
			</Flex.Col>

			<!-- Announcement Goes Here -->
			{#if event.announcement.text !== ""}
				<Flex.Col class="box-border p-8 rounded-3xl text-white gap-4 bg-app">
					<Flex.Row class="gap-3 items-center ">
						<!-- Icon -->
						 <IconAnnounce class="text-white size-8"/>
						<h3 >Announcements</h3>
					</Flex.Row>
					<h4 class="!opacity-100 !text-white/100">{event.announcement.text}</h4>
				</Flex.Col>
			{/if}
		</Flex.Col>

		<!-- Page Content Goes Here -->
		<Flex.Col class="pb-8">
			{@html event?.content.blueprint}
		</Flex.Col>

		{#if event.program}
			<ProgramLink slug={event.program}/>
		{/if}

		{#if asAdmin}
			<Edit/>
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
</style>
