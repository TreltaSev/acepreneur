import { get_preference, has_preference, set_preference } from '@root/lib/internal';
import { authform, fetch_backend, jsonform } from '@root/lib/internal/fetch';

export class User {
	constructor() {}

	/**
	 * Requests a user id from the backend server only if there is no specified user-id
	 */
	public async request_identity() {
		if ((await has_preference('identity')) && (await get_preference('identity')) != 'undefined') {
			console.info(
				`[user] Present user-id, skipping request identity`,
				await get_preference('identity')
			);
			return;
		}

		// Identification not specified, request a new one
		const response = await fetch_backend('/user', jsonform('POST'));

		console.log(response);

		if (response.status != 200) {
			console.error('Failed to request identity', response.data);
			return;
		}

		await set_preference('identity', response.data.id);
	}

	public async get_events() {
		const response = await fetch_backend('/events', await authform('GET'));
		console.log(response);
	}
}
