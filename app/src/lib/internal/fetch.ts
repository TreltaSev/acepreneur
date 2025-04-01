import { get_local, has_local } from './object';

const vite_api_url = import.meta.env.API_URL || 'https://localhost';

/* eslint-disable @typescript-eslint/no-explicit-any */
export function jsonform(method: string, object: BodyInit | null = null): RequestInit {
	const _obj: RequestInit = {
		method: method,
		headers: {
			'Content-Type': 'application/json'
		},
		mode: 'cors'
	};

	if (object) {
		_obj.body = JSON.stringify(object);
	}

	return _obj;
}

export function authform(method: string, object: BodyInit | null = null): RequestInit {
	const _obj = jsonform(method, object);

	if (!has_local('identification') || get_local("identification") == "undefined") {
		throw new Error('No identification found in local storage');
	}

	Object.assign(_obj.headers as any, { Bearer: get_local('identification') });

	return _obj;
}

export class HandledResponse {
	public request: Response | undefined;

	/**
	 * Handles the response from a request
	 * @param request Request Object
	 */
	constructor(request: Promise<Response> | Response) {
		if (!request) {
			throw new TypeError('Request Invalid');
		}

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
	 * Returns a boolean representing if the response object is a json object
	 */
	get isjson() {
		if (!this.request) return false;
		const contentType = this.request.headers.get('content-type');
		if (contentType && contentType.includes('application/json')) {
			return true;
		}
		return false;
	}

	get status() {
		return this.request?.status;
	}

	/**
	 * Returns the json from the request object
	 * @returns Json object or null if request is invalid or isn't json
	 */
	public async json(): Promise<null | any> {
		if (!this.request) return null;
		if (!this.isjson) return null;
		return await this.request.clone().json();
	}

	/**
	 * Returns the text from the request object
	 * @returns Text object or null if request is invalid
	 */
	public async text(): Promise<string | null> {
		if (!this.request) return null;
		return await this.request.clone().text();
	}
}

/**
 * Very low level fetch request
 * @param route
 * @param request_init
 * @returns
 */
export async function fetch_base(
	route: string,
	request_init?: RequestInit
): Promise<HandledResponse> {
	if (!request_init) {
		request_init = jsonform('GET', null);
	}
	const request = await fetch(route, request_init);
	const response = new HandledResponse(request);
	return response;
}

/**
 * Higher level fetch request that sends a request to the env-specified api_url
 * @param pathname
 * @param request_init
 * @returns
 */
export async function fetch_backend(
	pathname: string,
	request_init?: RequestInit
): Promise<HandledResponse> {
	if (!request_init) {
		request_init = jsonform('GET', null);
	}
	const request = await fetch(`${vite_api_url}/api${pathname}`, request_init);
	const response = new HandledResponse(request);
	return response;
}

/**
 * Throws an error if the response object isn't a json type.
 * @param response Json response
 * @returns
 */
export async function parse_json(response: HandledResponse) {
	if (!response.isjson) throw new TypeError('Response not json object: ' + response.request?.text);
	return await response.json();
}
