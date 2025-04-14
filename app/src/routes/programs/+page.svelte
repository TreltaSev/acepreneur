<script lang="ts">
    // --- Components ---
    import { ProgramCard } from './_components';

    // --- Logic ---
    import { getIdentityCtx } from '@root/lib/ctx';
    import type { Program } from '@internal/types';
    import { onMount } from 'svelte';
    import { Flex } from '@root/lib/ui';

    // Gathering user object from the identity context
    const { user } = getIdentityCtx();

    // Reactive States to handle what should be rendered
    let cached_programs: Program[] = $state([]);
    let loaded: boolean = $state(false);

    // Fetch the programs on load
    onMount(async () => {
        const programs = await user.get_programs();
        cached_programs = programs; // Save Programs
        cached_programs = cached_programs.sort((a, b) => {
            return (
                Number(a.order ?? Infinity) -
                Number(b.order ?? Infinity)
            );
        });
        loaded = true; // Stop "Loading"
    });
</script>

<h1>Programs</h1>

{#if !loaded}
    <!-- Loading -->
    <span>We are fetching the programs for you!</span>
{/if}

{#if loaded}
    {#if cached_programs.length == 0}
        <!-- No Programs, Display some error message -->
        <span>No programs found, try again later :)</span>
    {:else}
        <!-- Programs found, display programs-->
        <Flex.Col class="gap-20 mt-10 mb-20">
            {#each cached_programs as program}
                <ProgramCard data={program} />
            {/each}
        </Flex.Col>
    {/if}
{/if}