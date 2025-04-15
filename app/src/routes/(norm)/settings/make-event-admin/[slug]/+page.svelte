<script lang="ts">
	// --- Components ---
	import { Flex } from '@root/lib/ui';

	// --- Logic ---
	import { onMount } from 'svelte';
	import { getIdentityCtx } from '@root/lib/ctx';
	import { State } from '@internal/state.svelte';
	import type { Event } from '@internal/types';

	// Slug data object
	import { page } from '$app/state';
	import { authform, fetch_backend } from '@root/lib/internal/fetch';
	const slug = page.params.slug;

	// Gather user object from the identity context
	const { user } = getIdentityCtx();

	// Reactive State to store event information
	let event: Event | undefined = $state(undefined);
	let load_state = $state(new State());
	const api_url = import.meta.env.VITE_API_URL

	let code_url: string | undefined = $state(undefined)

	// Fetch the specified event on load
	onMount(async () => {
		const response = await fetch_backend('/event/admin/generate', await authform('POST', { slug } as unknown as BodyInit));
		if (response.status != 200) return;
		const code = response.data.secret.secret;
		const url = `https://finalfinance.us/api/qr/redeem-event-secret:${code}`
		code_url = url
		load_state.value="loaded"
	});
</script>

{#if load_state.value == 'loading'}
	<h2>Generating QR Code</h2>
	<h3>For {slug}</h3>
{/if}

{#if load_state.value == 'error'}
	<h2>Failed to generate</h2>
{/if}

{#if load_state.value == 'loaded'}
	<h1>Generated QR Code</h1>
	<h3>For {slug}</h3>
	<img alt="qr-code" src={code_url}/>
{/if}
