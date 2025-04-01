<script>
	// --- Components ---
	import { Button } from '@components';
	import qrCodeResponseHandler from '@root/lib/internal/qr/qr';

	// --- Icons ---
	import IconQRCode from '~icons/solar/qr-code-bold';
	import IconTrash from '~icons/solar/trash-bin-trash-bold';

	async function qr_prompt() {
		await qrCodeResponseHandler.prompt();
	}
</script>

<main>
	<h1>Settings</h1>

	<section>
		<h2>User</h2>
		<article>
			<summary>
				<h3>Change User ID</h3>
				<h4>Set your current user id to test specific functions</h4>
			</summary>

			<Button class="text-black/80" mode="outline" text="Scan" onclick={qr_prompt}>
				<IconQRCode />
			</Button>
		</article>

		<article>
			<summary>
				<h3>Delete User ID</h3>
				<h4>Delete your current user id and refresh to get a new one</h4>
			</summary>

			<aside>
				<Button class="text-red" mode="outline" text="Delete">
					<IconTrash />
				</Button>
			</aside>
		</article>

		<article>
			<summary>
				<h3>Current User ID</h3>
				<h4>user-c6d09d5fddfdc1c56a983a53e0f8a0d9</h4>
			</summary>
		</article>
	</section>

	<hr />

	<section>
		<h2>Developer</h2>
		<article>
			<summary>
				<h3>Developer Admin Token</h3>
				<h4>
					Set your admin token for administrator access to the backend server as well as the rest of
					this app
				</h4>
			</summary>

			<aside>
				<Button class="text-black/80" mode="outline" text="Scan">
					<IconQRCode />
				</Button>
			</aside>
		</article>

		<article>
			<summary>
				<h3>Enable Admin Access</h3>
				<h4>Toggle Admin Access towards resources, when toggled, refreshes the current user id.</h4>
			</summary>
			<aside>
				<Button class="text-black/80" mode="outline" text="Scan">
					<IconQRCode />
				</Button>
			</aside>
		</article>
	</section>
</main>

<style scoped>
	/* Style Main */
	main {
		@apply flex flex-col box-border;
		gap: calc(var(--spacing) * 9);
		padding: calc(var(--spacing) * 10);
		overflow-y: auto;
	}

	section {
		@apply flex flex-col;
		gap: calc(var(--spacing) * 5);
	}

	/* Style Individual Setting Options */
	article {
		@apply flex flex-row items-start justify-between;

		/* Remove Summary Marker */
		list-style: none;

		gap: calc(var(--spacing) * 12);
	}

	article > *:not(summary) {
		margin-top: 3rem;
	}
</style>
