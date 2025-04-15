<script lang="ts">
	import { clamp } from '@root/lib/internal';
	import 'pinch-zoom-element';
	import { onMount } from 'svelte';
	let pinchZoom: undefined | any;

	onMount(() => {
		// The docs are so scuffed bro, had to use the source code :sob:
		pinchZoom.scaleTo(0.9, {
			originX: '50%',
			originY: '30%',
			relativeTo: 'container',
			allowChangeEvent: true
		});
	});
</script>

<pinch-zoom bind:this={pinchZoom}>
	<div>
		<img
			src="https://core-docs.s3.amazonaws.com/henrico_county_public_schools_ar/picture/data/774085/content_7DA_-4IwbOH4l_lkasPTfw.jpeg"
			alt="a"
			class="rounded-2xl"
		/>

		<h3 class="absolute -bottom-30 left-0">
			Pinch to move<br />
			<a class="text-app" href="https://entrepreneurship-day.github.io/index.html"
				>Click here to visit the website</a
			>
		</h3>
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
