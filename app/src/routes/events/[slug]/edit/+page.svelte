<script lang="ts">
	// --- Logic ---
	import { goto } from '$app/navigation';

	// Slug data object
	import { page } from '$app/state';
	const slug = page.params.slug;
</script>

<span>Editing here for {slug}</span>
