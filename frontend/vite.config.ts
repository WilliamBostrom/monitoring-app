import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	define: {
		// Definiera miljövariabler som ska vara tillgängliga i klienten
		'import.meta.env.VITE_API_URL': JSON.stringify(
			process.env.VITE_API_URL || 'http://127.0.0.1:8000'
		)
	}
});
