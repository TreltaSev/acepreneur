import { get, writable, type Writable } from "svelte/store";

class ModeManager {

    mode$: Writable<string> = writable("light");

    constructor() {
        if (typeof window === 'undefined') return;        
        const local_mode: string | null = localStorage.getItem("mode")
        this.mode$.set(local_mode || "dark")
    }   

    get mode() {
        return get(this.mode$)
    }

    toggle() {        
        const isDark = this.mode == "dark";
        this.mode$.set(isDark ? "light" : "dark")
        localStorage.setItem("mode", this.mode)
    }
}

export const global_mode$ = new ModeManager();