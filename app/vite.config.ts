import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import Icons from 'unplugin-icons/vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, '../');

	return {
		plugins: [
			tailwindcss(),
			sveltekit(),
			Icons({ autoInstall: true, compiler: 'svelte' }),
			SvelteKitPWA({
				strategies: 'generateSW',
				srcDir: 'src',
				filename: 'service-worker.js',
				manifest: {
					name: 'Acepreneur',
					short_name: 'App',
					start_url: '/',
					display: 'standalone',
					background_color: '#ffffff',
					theme_color: '#8658F1',
					icons: [
						{
							src: '/icons/icon-192.png',
							sizes: '192x192',
							type: 'image/png'
						},
						{
							src: '/icons/icon-512.png',
							sizes: '512x512',
							type: 'image/png'
						}
					]
				}
			})
		],
		define: {
			'process.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL)
		}
	};
});
