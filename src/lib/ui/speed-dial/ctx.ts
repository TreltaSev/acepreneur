import { getContext, setContext } from 'svelte';
import { toggle_writable, type ToggleableWritable } from '@lib/internal/store';
import { removeUndefined } from '@lib/internal';
import type { tSpeedDialMenuProps } from './types';

export function createSpeedDial(props: tSpeedDialMenuProps) {
	const isActive$: ToggleableWritable = toggle_writable(false);

	return {
		...props,
		isActive$,
	};
}

export function getSpeedDialData() {
	const NAME = 'speed-dial' as const;

	return {
		NAME
	};
}

export function setCtx(props: tSpeedDialMenuProps = {}) {
	const { NAME } = getSpeedDialData();

	const speedDial = {
		...createSpeedDial({ ...removeUndefined(props) })
	};

	setContext(NAME, speedDial);

	return {
		...speedDial
	};
}

type GetReturn = ReturnType<typeof setCtx>;
export function getCtx() {
	const { NAME } = getSpeedDialData();
	return getContext<GetReturn>(NAME);
}