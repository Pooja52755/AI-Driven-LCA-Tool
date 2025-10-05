import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 5000,
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true
			}
		}
	},
	build: {
		target: 'es2020',
		rollupOptions: {
			output: {
				manualChunks: {
					'vis': ['vis-network', 'vis-data'],
					'charts': ['chart.js']
				}
			}
		}
	}
});