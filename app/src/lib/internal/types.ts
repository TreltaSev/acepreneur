/**
 * User type that the client would see
 */
/**
 * Represents a user in the system with various properties such as ID, name, and likes.
 */
export type User = {
    /**
     * A unique identifier for the user.
     */
    id: number;

    /**
     * The name of the user.
     */
    name: string;

    /**
     * A list of interests or preferences associated with the user.
     */
    likes: string[];
};

/**
 * Event type that the client would see, likes are sanitized.
 */
/**
 * Represents an event with various properties such as metadata, content, and reactions.
 */
export type Event = {
    /**
     * The order of the event, used for sorting or prioritization.
     * Optional.
     */
    order?: number;

    /**
     * The name of the event.
     */
    name: string;

    /**
     * A brief description of the event.
     */
    description: string;

    /**
     * Information about the event's card, including its appearance.
     */
    card: {
        /**
         * The color of the card, typically represented as a CSS color string.
         */
        color: string;

        /**
         * Details about the image displayed on the card.
         */
        image: {
            /**
             * The URL of the image.
             */
            url: string;

            /**
             * An optional CSS class to style the image.
             */
            _class?: string;

            /**
             * Optional inline CSS styles for the image.
             */
            style?: string;
        };
    };

    /**
     * A unique identifier for the event, typically used in URLs.
     */
    slug: string;

    /**
     * The main content of the event.
     */
    content: {
        /**
         * A blueprint or template string representing the event's content structure.
         */
        blueprint: string;
    };

    /**
     * A list of tags associated with the event for categorization or filtering.
     */
    tags: string[];

    /**
     * Information about the event's announcement.
     */
    announcement: {
        /**
         * The content of the announcement.
         */
        content: string;

        /**
         * The author of the announcement.
         */
        author: string;

        /**
         * The time the announcement was made, typically in ISO 8601 format.
         */
        time: string;
    };

    /**
     * Reactions to the event, including likes.
     */
    reactions: {
        /**
         * The number of likes or an array of user identifiers who liked the event.
         */
        likes: number | string[];
    };

    /**
     * A list of administrators associated with the event.
     * Optional.
     */
    admins?: string[];
};

/**
 * Represents a program with various properties such as order, name, description, card details, slug, and content.
 */
export type Program = {
	/**
	 * The order of the program. Optional.
	 */
	order?: number;

	/**
	 * The name of the program.
	 */
	name: string;

	/**
	 * A brief description of the program.
	 */
	description: string;

	/**
	 * Details about the program's card, including color and image.
	 */
	card: {
		/**
		 * The color of the card.
		 */
		color: string;

		/**
		 * Information about the image displayed on the card.
		 */
		image: {
			/**
			 * The URL of the image.
			 */
			url: string;

			/**
			 * An optional CSS class for the image.
			 */
			_class?: string;

			/**
			 * Optional inline styles for the image.
			 */
			style?: string;
		};
	};

	/**
	 * The unique slug identifier for the program.
	 */
	slug: string;

	/**
	 * The content details of the program, including a blueprint.
	 */
	content: {
		/**
		 * The blueprint of the program's content.
		 */
		blueprint: string;
	};
};
