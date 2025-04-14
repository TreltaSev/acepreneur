<script lang="ts">
	import 'pinch-zoom-element';
	import { onMount } from 'svelte';
	let pinchZoom: undefined | any;

   onMount(() => {
    console.log(pinchZoom)
   })
</script>

<pinch-zoom bind:this={pinchZoom}>
	<div>
		<img
			src="https://core-docs.s3.amazonaws.com/henrico_county_public_schools_ar/picture/data/774085/content_7DA_-4IwbOH4l_lkasPTfw.jpeg"
			alt="a"
		/>

		<h3 class="absolute -bottom-15 left-0">Too Small? Zoom In!</h3>
	</div>
</pinch-zoom>

<style>
	pinch-zoom {
		display: block;
		width: 100%;
		height: 100%;
		overflow: hidden;
		touch-action: none;
	}
</style>
