const isProduction = typeof window !== 'undefined' && window.location.hostname !== 'localhost';

// Access environment variables through global Vite object
const viteEnv = (globalThis as any).import?.meta?.env || {};

export const API_URL = isProduction
	? viteEnv.VITE_HOST_API_URL || 'http://100.65.174.56:3000' // Use VITE_HOST_API_URL for Pi
	: viteEnv.VITE_API_URL || 'http://localhost:3000'; // Use VITE_API_URL for local
