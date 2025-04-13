<script>
    // Slug data object
	import { page } from '$app/state';

    const slug = page.params.slug;
</script>

<h2>You are now an admin!</h2>
<h3>What does that mean?</h3>
<h4>Well, that means now you can edit the announcements board for the event with the id {slug}</h4>