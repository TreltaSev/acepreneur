import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import Icons from 'unplugin-icons/vite';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, '../')
	console.log(env)
	return {
		plugins: [tailwindcss(), sveltekit(), Icons({ autoInstall: true, compiler: 'svelte' })],
		define: {
			'process.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL)
		},
	};
});
