import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
			pages: 'www',
			assets: 'www',
			fallback: 'index.html'
		}),

		paths: {
			base: process.argv.includes("dev") ? '' : process.env.BASE_PATH
		},

		alias: {
			"@root": "src/",
			"@lib": "src/lib",
			"@ui": "src/lib/ui",
			"@components": "src/lib/components"
		}
	}
};

export default config;
