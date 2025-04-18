<script lang="ts">
	// --- Components ---
	import { AdminOnly, Button, Toggle } from '@components'; // Importing reusable button and toggle components
	import { getIdentityCtx } from '@root/lib/ctx'; // Fetching user identity context
	import { get_preference, set_preference } from '@root/lib/internal'; // Methods to get/set user preferences
	import qrCodeResponseHandler from '@root/lib/internal/qr/qr'; // QR code handling logic

	// --- Icons ---
	import IconQRCode from '~icons/solar/qr-code-bold'; // QR code icon
	import IconTrash from '~icons/solar/trash-bin-trash-bold'; // Trash/delete icon

	// Get user identity context
	const { identity$, dev_admin$, user } = getIdentityCtx();

	// Reactive state for admin access status
	let active_admin: boolean | null = $state(null);
	dev_admin$.subscribe((c) => (active_admin = c));

	// True whenever the admin toggle is toggled
	let admin_toggled: boolean | null = $derived(active_admin);

	async function flop() {
		// If admin secret is not valid, force toggle to be false
		if (!active_admin) {
			admin_toggled = false;
		}
	}

	// Function to handle QR code prompt for scanning user ID or admin token
	async function qr_prompt() {
		await qrCodeResponseHandler.prompt();
	}

	// Function to delete the current user ID and refresh identity
	async function delete_user() {
		await user.refresh_identity();
	}

	// Update admin access state and save preference
	async function onupdate(value: boolean) {
		admin_toggled = value;

		console.error(`UPDATE: VALUE: ${value}`);

		if (await user.admin_valid()) {
			console.log(
				`Admin token is valid: ${value} ${typeof value} ${JSON.stringify(value)} ${typeof JSON.stringify(value)}`
			);
			await set_preference('dev-admin', JSON.stringify(value));
			await user.refresh_identity();
		} else {
			console.log(`Admin token is invalid: ${value} ${typeof value} ${JSON.stringify(value)}`);
		}
	}
</script>

<main class="pb-20 overflow-y-visible">
	<h1>Settings</h1>

	<!-- User Settings Section -->
	<section>
		<h2>User</h2>

		<!-- Change User ID -->
		<article>
			<summary>
				<h3>Change User ID</h3>
				<h4>Set your current user ID to test specific functions</h4>
			</summary>

			<Button class="text-black/80" mode="outline" text="Scan" onclick={qr_prompt}>
				<IconQRCode />
			</Button>
		</article>

		<!-- Delete User ID -->
		<article>
			<summary>
				<h3>Delete User ID</h3>
				<h4>Delete your current user ID and refresh to get a new one</h4>
			</summary>

			<aside>
				<Button class="text-red" mode="outline" text="Delete" onclick={delete_user}>
					<IconTrash />
				</Button>
			</aside>
		</article>

		<!-- Display Current User ID -->
		<article>
			<summary>
				<h3>Current User ID</h3>
				<h4>{$identity$ || 'Generating'}</h4>
			</summary>
		</article>
	</section>

	<hr />

	<!-- Developer Settings Section -->
	<section>
		<h2>Developer</h2>

		<!-- Developer Admin Token -->
		<article>
			<summary>
				<h3>Developer Admin Token</h3>
				<h4>
					Set your admin token for administrator access to the backend server as well as the rest of
					this app
				</h4>
			</summary>

			<aside>
				<Button class="text-black/80" mode="outline" text="Scan" onclick={qr_prompt}>
					<IconQRCode />
				</Button>
			</aside>
		</article>

		<!-- Enable Admin Access -->
		<article>
			<summary>
				<h3>Enable Admin Access</h3>
				<h4>Toggle Admin Access towards resources. When toggled, refreshes the current user ID.</h4>
			</summary>
			<aside>
				<Toggle {onupdate} value={admin_toggled || false} ontrue={flop} />
			</aside>
		</article>
	</section>

	<AdminOnly>
		<!-- Events Settings Section -->
		<section>
			<h2>Events</h2>

			<!-- Event Admin Setup -->
			<article>
				<summary>
					<h3>Event Admin Setup</h3>
					<h4>
						Generate a QR Code for a specific event that someone can scan and become a event-admin
					</h4>
				</summary>

				<aside>
					<Button class="text-black/80" mode="outline" text="Gen" href="/settings/make-event-admin">
						<IconQRCode />
					</Button>
				</aside>
			</article>
		</section>
	</AdminOnly>
</main>

<style scoped>
	/* Style Main */
	main {
		@apply flex flex-col box-border;
		gap: calc(var(--spacing) * 9);
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
