<script lang="ts">
	import { getIdentityCtx } from "@root/lib/ctx";
	import { onMount } from "svelte";

    const {user} = getIdentityCtx();

    const cached_events: any = $state([])

    onMount(async () => {
        const events = await user.get_events();
        
        console.log(events)


    
    })
</script>

<h1>Events</h1>