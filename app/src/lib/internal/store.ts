/* eslint-disable @typescript-eslint/no-explicit-any */
import { writable, type Writable, type Subscriber, type Unsubscriber, type Updater} from "svelte/store";

export class ToggleableWritable implements Writable<boolean> {
    private store: Writable<boolean>

    constructor(initialValue: boolean) {
        this.store = writable(initialValue)
    }

    /**
     * Toggles the value of the store
     * 
     * @param {MouseEvent | boolean | null} value - Value the store will be set to, if this is null, assume toggle
     */
    toggle(value: MouseEvent | boolean | null = null): void {
        if (value instanceof MouseEvent || value === null) {
            this.store.update(currentValue => !currentValue)
        } else {
            this.store.set(value)
        }
    }

    subscribe(run: Subscriber<boolean>, invalidate?: () => void): Unsubscriber {
        return this.store.subscribe(run, invalidate)
    }

    set(value: boolean): void {
        this.store.set(value)
    }

    update(updater: Updater<boolean>): void {
        this.store.update(updater)
    }
}

export function toggle_writable(initialValue: boolean): ToggleableWritable {
    return new ToggleableWritable(initialValue);
}

type Options = Record<string, Writable<unknown>>;
export function getOptionUpdater(options: Options) {
    return function(key: keyof typeof options, value: any) {
        if (value === undefined) return;
        const store = options[key];
        if (store) {
            store.set(value as never)
        }
    }
}