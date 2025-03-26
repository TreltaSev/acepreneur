<script lang="ts">
	import { Navigation } from '@components';
	import { Flex, Page, Span } from '@ui';
</script>

<Page.Root>
	<Flex.Col class="size-full items-center justify-center">
		<span>And this will be where the map is located</span>

		<button
			onclick={() => (window.location.href = '/')}
			class="px-6 py-2 rounded-md justify-center items-center text-white bg-primary">Go Back</button
		>
	</Flex.Col>
</Page.Root>
