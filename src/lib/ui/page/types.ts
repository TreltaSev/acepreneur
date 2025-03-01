import type { HTMLAttributes } from 'svelte/elements';

export type tPageProps = HTMLAttributes<HTMLDivElement> & {
    hideNav?: boolean
}

export type tPageNavigationProps = HTMLAttributes<HTMLDivElement>;
