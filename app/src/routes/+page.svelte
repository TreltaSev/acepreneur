<script lang="ts">
	import { Navigation } from '@components';
	import { Flex, Page, Span } from '@ui';

	import SolarBookmarkBold from '~icons/solar/bookmark-bold';
	import SolarHomeSmileBold from '~icons/solar/home-smile-bold';
	import SolarBombBold from '~icons/solar/bomb-bold';
	import SolarMapBold from '~icons/solar/map-bold';
	import SolarQrCodeBold from '~icons/solar/qr-code-bold';
</script>

<Page.Root>
	<Flex.Col class="size-full items-center justify-center">
		<span>Hi There!</span>
	</Flex.Col>

	<Navigation.Root class="border-black/20 border-t items-center justify-center">
		<Navigation.Item href="/" class="text-primary">
			{#snippet icon()}
				<SolarHomeSmileBold />
			{/snippet}
			<span>Home</span>
		</Navigation.Item>

		<Navigation.Item href="/other" class="text-secondary">
			{#snippet icon()}
				<SolarBombBold />
			{/snippet}
			<span>Home</span>
		</Navigation.Item>

		<Navigation.Item class="text-white bg-primary size-fit p-2 box-border mx-4 rounded-lg" onclick={() => {console.log("Click :)")}}>
			{#snippet icon()}
				<SolarQrCodeBold class="size-7"/>
			{/snippet}
		</Navigation.Item>

		<Navigation.Item class="text-secondary"  href="/other2">
			{#snippet icon()}
				<SolarBookmarkBold />
			{/snippet}
			<span>Other</span>
		</Navigation.Item>

		<Navigation.Item class="text-primary"  href="/map">
			{#snippet icon()}
				<SolarMapBold />
			{/snippet}
			<span>Map</span>
		</Navigation.Item>
	</Navigation.Root>
</Page.Root>
