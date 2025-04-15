<script lang="ts">
	// --- Logic ---
	import { goto } from '$app/navigation';

	// Slug data object
	import { page } from '$app/state';
	import { Button } from '@root/lib/components';
	import { getIdentityCtx } from '@root/lib/ctx';
	import { State } from '@root/lib/internal';
	import type { Event, Program } from '@root/lib/internal/types';
	import { Flex } from '@root/lib/ui';
	import { onMount } from 'svelte';
	const slug = page.params.slug;

	let event: Event | undefined = $state(undefined);
	let load_state: State = $state(new State());
	let input_value: string | undefined = $state(undefined);

	const { user } = getIdentityCtx();

	onMount(async () => {
		event = await user.get_event(slug);
		load_state.flagLoaded();
		input_value = event?.announcement.text
	});

	async function set() {
		if (!event) return;
		if (!input_value) {input_value = ""};
		if (!event.id) return;
		await user.set_announcement(event.id, input_value)
		window.location.reload();
	}

	async function clear() {
		if (!event) return;
		if (!event.id) return;
		await user.set_announcement(event.id, "")
		window.location.reload()
	}
</script>

{#if load_state.value == 'loading'}
	<h3>Loading Data for {slug}</h3>
{/if}

{#if load_state.value == 'loaded' && event}
	<Flex.Col class="gap-8 size-full">
		<h3>Loaded</h3>
		<section class="w-full">
			<h4>Announcements</h4>
			<textarea bind:value={input_value} id="textarea" class="p-5 border border-black/40 rounded-2xl text-2xl w-full min-h-20 max-h-60"></textarea>
		</section>
		<Flex.Col class="gap-10">
			<Button class="text-black w-full" mode="outline" text="Save Announcements" onclick={set}/>
			<Button class="text-red w-full" mode="outline" text="Clear Announcements" onclick={clear}/>
		</Flex.Col>
		<span class="text-sm"><i>Not my best work</i></span>
	</Flex.Col>
{/if}
