/**
 * User type that the client would see
 */
export type User = {
    id: number;
    name: string;
    likes: string[];
}


/**
 * Event type that the client would see, likes are sanitized.
 */
export type Event = {
	order?: number;
    name: string;
    description: string;
    card: {
        color: string;
        image: {
            url: string;
            _class?: string;
            style?: string;
        }
    };
    slug: string;
    content: {
        blueprint: string;
    },
    tags: string[];
    announcement: {
        content: string;
        author: string;
        time: string;
    };
    reactions: {
        likes: number | string[];
    };
    admins?: string[]
}