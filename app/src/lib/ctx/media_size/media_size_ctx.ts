/* eslint-disable @typescript-eslint/no-explicit-any */
import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';

export function createMediaData() {
	const medias = {
		xs: (x: number) => x < 640,
		sm: (x: number) => x >= 640,
		lg: (x: number) => x >= 768,
		xl: (x: number) => x >= 1280,
		'2xl': (x: number) => x >= 1536
	};

	function get_media() {
		let media_buff: string = 'xs';
		Object.entries(medias).forEach(([key, value]) => {
			if (value(window.innerWidth)) {
				media_buff = key;
			}
		});
		return media_buff;
	}

	function set_media() {
		media$.set(get_media());
	}

	const media$: Writable<string | undefined> = writable(undefined);

	return {
		media$,
		get_media,
		set_media
	};
}

export function getMediaData() {
	const NAME = 'media-data' as const;

	return {
		NAME
	};
}

export function setMediaCtx() {
	const { NAME } = getMediaData();

	const media = {
		...createMediaData()
	};

	setContext(NAME, media);

	return {
		...media
	};
}

type GetMediaReturn = ReturnType<typeof setMediaCtx>;
export function getMediaCtx() {
	const { NAME } = getMediaData();
	return getContext<GetMediaReturn>(NAME);
}
