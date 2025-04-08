<script lang="ts">
	// --- Components ---

	// --- Logic ---
	import { onMount } from 'svelte';
	import { getIdentityCtx } from '@root/lib/ctx';

    // Slug data object
    import { page } from "$app/state";
    const slug = page.params.slug

	// Gather user object from the identity context
    const { user } = getIdentityCtx()

	// Reactive State to store event information

	// Fetch the specified event on load
	onMount(async () => {
        // const event = await user.get_event(slug)

    });
</script>


<span>event ;)</span>