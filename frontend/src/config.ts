const mode = import.meta.env.MODE; // ger "development" eller "production"

export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Debug: visa vad som används
console.log('Mode:', mode);
console.log('VITE_API_URL:', import.meta.env.VITE_API_URL);
console.log('Final API_URL:', API_URL);
