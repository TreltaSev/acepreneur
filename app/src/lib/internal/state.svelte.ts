/* eslint-disable @typescript-eslint/no-explicit-any */
export type tProgress = 'loading' | 'loaded' | 'error';

/**
 * Represents a generic state handler to track loading progress and store a contextual value.
 *
 * This class is useful for managing UI states such as loading, loaded, or error,
 * and associating additional context data alongside it.
 */
export class State {
	/**
	 * Arbitrary context associated with this state.
	 * Can be used to store component-specific or app-specific data.
	 */
	public ctx: any = $state(undefined);

	/**
	 * Represents the current progress status.
	 * Can be one of: "loading", "loaded", or "error".
	 */
	public value: tProgress = $state('loading');

	/**
	 * Marks the current state as an error.
	 */
	public flagError() {
		this.value = 'error';
	}

	/**
	 * Marks the current state as successfully loaded.
	 */
	public flagLoaded() {
		this.value = 'loaded';
	}

	/**
	 * Marks the current state as loading.
	 */
	public flagLoading() {
		this.value = 'loading';
	}

	/**
	 * Sets the context value.
	 * @param v - Any data to be associated as context.
	 */
	public setCtx(v: any) {
		this.ctx = v;
	}
}
