import { CapacitorHttp, type HttpOptions, type HttpResponse } from '@capacitor/core';
import { get_preference, has_preference } from './object';

const vite_api_url = import.meta.env.VITE_API_URL || 'https://localhost';

/* eslint-disable @typescript-eslint/no-explicit-any */

/**
 * Creates a basic HTTP request object with JSON headers.
 *
 * @param {string} method - HTTP method (e.g., 'GET', 'POST', etc.).
 * @param {BodyInit | null} object - Optional request body.
 *
 * @returns {Omit<HttpOptions, 'url'>} An HTTP options object without the URL.
 */
export async function jsonform(method: string, object: BodyInit | null = null): Promise<Omit<HttpOptions, 'url'>> {
	const _obj: Omit<HttpOptions, 'url'> = {
		method: method,
		headers: {
			'Content-Type': 'application/json'
		},
		webFetchExtra: {
			mode: 'cors'
		}
	};

	// Add admin token if present
	if (await has_preference('admin_token') && (await get_preference("admin_active") == "true")) {
		Object.assign(_obj.headers as any, { 'Admin-Token': await get_preference('admin_token') });
	}

	if (object) {
		_obj.data = JSON.stringify(object);
	}

	return _obj;
}

/**
 * Creates an authenticated HTTP request object.
 *
 * Adds user identity and admin token (if available) as headers.
 *
 * @param {string} method - HTTP method (e.g., 'GET', 'POST', etc.).
 * @param {BodyInit | null} object - Optional request body.
 *
 * @throws {Error} If no user identity is found in preferences.
 *
 * @returns {Promise<Omit<HttpOptions, 'url'>>} An authenticated HTTP options object.
 */
export async function authform(
	method: string,
	object: BodyInit | null = null
): Promise<Omit<HttpOptions, 'url'>> {
	const _obj = await jsonform(method, object);

	// Ensure identity is available
	if (!(await has_preference('identity')) || (await get_preference('identity')) === 'undefined') {
		throw new Error('No identification found in local storage');
	}

	// Add user identity token
	Object.assign(_obj.headers as any, { Bearer: await get_preference('identity') });

	// Add admin token if present
	if (await has_preference('admin_token')) {
		Object.assign(_obj.headers as any, { 'Admin-Token': await get_preference('admin_token') });
	}

	return _obj;
}

/**
 * Wrapper for handling HTTP responses.
 */
export class HandledResponse {
	public request: Response | undefined;

	/**
	 * Constructs a HandledResponse from a given request.
	 *
	 * @param {Promise<Response> | Response} request - The request response object.
	 *
	 * @throws {TypeError} If the request is invalid.
	 */
	constructor(request: Promise<Response> | Response) {
		if (!request) {
			throw new TypeError('Request Invalid');
		}

		// Handle promises and store response when resolved
		if (typeof (request as Promise<Response>).then === 'function') {
			(request as Promise<Response>)
				.then((res) => {
					this.request = res;
				})
				.catch((err) => {
					throw new Error('Failed to resolve request: ' + err);
				});
		} else {
			this.request = request as Response;
		}
	}

	/**
	 * Checks if the response is a JSON object.
	 *
	 * @returns {boolean} `true` if the response contains JSON, otherwise `false`.
	 */
	get isjson(): boolean {
		if (!this.request) return false;
		const contentType = this.request.headers.get('content-type');
		return contentType ? contentType.includes('application/json') : false;
	}

	/**
	 * Gets the response status code.
	 *
	 * @returns {number | undefined} The HTTP status code.
	 */
	get status(): number | undefined {
		return this.request?.status;
	}

	/**
	 * Parses the response body as JSON.
	 *
	 * @returns {Promise<any | null>} The parsed JSON object or `null` if invalid.
	 */
	public async json(): Promise<any | null> {
		if (!this.request || !this.isjson) return null;
		return await this.request.clone().json();
	}

	/**
	 * Gets the response body as a text string.
	 *
	 * @returns {Promise<string | null>} The response text or `null` if invalid.
	 */
	public async text(): Promise<string | null> {
		if (!this.request) return null;
		return await this.request.clone().text();
	}
}

/**
 * Performs a low-level HTTP request using CapacitorHttp.
 *
 * @param {string} pathname - API route.
 * @param {Omit<HttpOptions, 'url'>} [request_init] - Optional request parameters.
 *
 * @returns {Promise<HttpResponse>} The HTTP response.
 */
export async function fetch_base(
	pathname: string,
	request_init?: Omit<HttpOptions, 'url'>
): Promise<HttpResponse> {
	if (!request_init) {
		request_init = await jsonform('GET', null);
	}

	const response = await CapacitorHttp.request({
		...request_init,
		url: `${vite_api_url}/api${pathname}`
	});
	return response;
}

/**
 * Sends a high-level HTTP request to the API server.
 *
 * This function is similar to `fetch_base` but follows environment-defined API settings.
 *
 * @param {string} pathname - API route.
 * @param {Omit<HttpOptions, 'url'>} [request_init] - Optional request parameters.
 *
 * @returns {Promise<HttpResponse>} The HTTP response.
 */
export async function fetch_backend(
	pathname: string,
	request_init?: Omit<HttpOptions, 'url'>
): Promise<HttpResponse> {
	if (!request_init) {
		request_init = await jsonform('GET', null);
	}

	const response = await CapacitorHttp.request({
		...request_init,
		url: `${vite_api_url}/api${pathname}`
	});
	return response;
}

/**
 * Ensures the response is a JSON object before parsing.
 *
 * @param {HandledResponse} response - The response to parse.
 *
 * @throws {TypeError} If the response is not JSON.
 *
 * @returns {Promise<any>} The parsed JSON response.
 */
export async function parse_json(response: HandledResponse): Promise<any> {
	if (!response.isjson) throw new TypeError('Response not json object: ' + response.request?.text);
	return await response.json();
}
