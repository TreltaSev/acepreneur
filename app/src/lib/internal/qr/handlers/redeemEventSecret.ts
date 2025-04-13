import { goto } from '$app/navigation';
import { authform, fetch_backend } from '@internal/fetch';

export async function redeemEventSecret(token: string) {
	const response = await fetch_backend(`/event/admin/redeem/${token}`, await authform('GET'));
	if (response.status !== 200) return;
	if (response.data.added) {
		console.log(`[redeemEventSecret] Event ${response.data.event} added`);
	}

    
	await goto(`/settings/ake-event-admin/${response.data.event.slug}/success`);
}
