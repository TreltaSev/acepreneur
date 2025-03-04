<script lang="ts">
    let { children } = $props();

    import "../app.css"

    import { global_mode$ } from '@lib/stores/mode';
	let mode$ = global_mode$.mode$;

	// Apply the class on subscription update
	// mode$.subscribe((v) => {
	// 	if (typeof document !== 'undefined') {
	// 		document.documentElement.classList.toggle('dark', v === 'dark');
	// 	}
	// });

</script>

<div class="white size-full">
    {@render children?.()}
</div> 



<style>
	:global(html, body) {
		width: 100%;
		height: 100%;
	}
</style>