<script lang="ts">

    // --- Logic ---
    import { cn } from '@lib/utils';
    import type { RowProps } from ".."
    
    let {
        children,
        class: className,
        rowClass = $bindable('flex flex-row'),
        ...rest
    }: RowProps = $props();


    // Setup Row's class
    let rowCls = $state(cn(rowClass, className));
    $effect(() => {
        rowCls = cn(rowClass, className)
    })

</script>

<div class={ rowCls } {...rest}>
    {@render children?.()}
</div>

<!--@component
    Generated by SvelteForge🔥
-->

