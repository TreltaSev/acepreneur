import type { PromptOptions } from '@capacitor/dialog';
import { delete_preference, get_preference, has_preference, set_preference } from '@internal';
import { authform, fetch_backend, jsonform } from '@internal/fetch';
import { type Event } from '@internal/types';

export class User {
	constructor() {}

	/**
	 * Requests a user ID from the backend server only if none is stored.
	 *
	 * If an identity is already stored in preferences and is not 'undefined',
	 * the request is skipped.
	 *
	 * @returns {Promise<void>} A promise that resolves once the identity request is handled.
	 */
	public async request_identity(): Promise<void> {
		// Check if an identity already exists in preferences
		if ((await has_preference('identity')) && (await get_preference('identity')) !== 'undefined') {
			console.info(
				`[user] Present user-id, skipping request identity`,
				await get_preference('identity')
			);
			return;
		}

		// No identity found, request a new one from the backend
		const response = await fetch_backend('/user', await jsonform('POST'));

		// Handle non-200 response status
		if (response.status !== 200) {
			console.error('Failed to request identity', response.data);
			return;
		}

		// Store the received identity in preferences
		await set_preference('identity', response.data.id);

		// Check if new identity includes dev admin perms
		const admin_response = await fetch_backend('/admin/is', await authform('GET'));
		if (admin_response.status == 200) {
			await set_preference('dev-admin', admin_response.data.state || false);
		}
	}

	/**
	 * Checks if the admin secret stored in preferences is valid
	 *
	 * @returns {Promise<boolean>} A promise that resolves with the confirmation of an admin secret being valid
	 */
	public async admin_valid(): Promise<boolean> {

		// No admin token to check
		if (!await has_preference("admin_token")) return false;

		const admin_response = await fetch_backend(
			'/admin/is',
			await jsonform('POST', { secret: await get_preference('admin_token') } as unknown as BodyInit)
		);

		if (admin_response.status !== 200) return false;

		// Response was recieved
		
		return true;
	}

	/**
	 * Clears the stored user identity and notifies the backend.
	 *
	 * Deletes the identity preference locally and sends a DELETE request to the backend
	 * if an identity was stored.
	 *
	 * @returns {Promise<void>} A promise that resolves once the identity is cleared.
	 */
	public async clear_identity(): Promise<void> {
		// Notify the backend that the identity has been removed
		await fetch_backend('/user', await authform('DELETE'));

		await delete_preference('identity'); // Remove identity from preferences
	}

	/**
	 * Refreshes the user identity by clearing the stored identity and requesting a new one.
	 *
	 * @returns {Promise<void>} A promise that resolves once the identity is refreshed.
	 */
	public async refresh_identity(): Promise<void> {
		await this.clear_identity(); // Remove the existing identity
		await this.request_identity(); // Request a new identity
	}

	/**
	 * Fetches events from the backend.
	 *
	 * Sends a GET request to the backend to retrieve event data.
	 *
	 * @returns {Promise<Event[]>} A promise that resolves when the events are fetched.
	 */
	public async get_events(): Promise<Event[]> {
		const response = await fetch_backend('/events', await authform('GET'));
		return response.data.events || [];
	}

	public async get_event(slug: string): Promise<Event | undefined> {
		const response = await fetch_backend(`/event/event-${slug}`, await authform('GET'));
		return response.data.event || undefined;
	}
}
