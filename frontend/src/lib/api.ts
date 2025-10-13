import { API_URL } from '../config';

// API-anrop för meny
export async function fetchMenu() {
	try {
		const res = await fetch(`${API_URL}/menu`);
		const data = await res.json();
		return data.options;
	} catch (err: any) {
		console.error('Fel vid hämtning av meny:', err.message);
		throw err;
	}
}

// API-anrop för menyval
export async function selectChoice(choice: number) {
	try {
		const res = await fetch(`${API_URL}/select`, {
			method: 'POST',
			body: JSON.stringify({ choice }),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await res.json();
		return data.result;
	} catch (err: any) {
		console.error('Fel vid menyval:', err.message);
		throw err;
	}
}

// API-anrop för alarm
export async function fetchAlarms() {
	try {
		const res = await fetch(`${API_URL}/alarms`);
		const data = await res.json();
		return data.alarms || [];
	} catch (err: any) {
		console.error('Fel vid hämtning av alarm:', err.message);
		throw err;
	}
}

export async function createAlarm(type: string, threshold: number) {
	try {
		const res = await fetch(`${API_URL}/alarms`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ type, threshold })
		});
		const data = await res.json();
		return data;
	} catch (err: any) {
		console.error('Fel vid skapande av alarm:', err.message);
		throw err;
	}
}

export async function deleteAlarm(alarmId: number) {
	try {
		const res = await fetch(`${API_URL}/alarms/${alarmId}`, {
			method: 'DELETE'
		});
		const data = await res.json();
		return data;
	} catch (err: any) {
		console.error('Fel vid borttagning av alarm:', err.message);
		throw err;
	}
}

export async function fetchAlarmStatus() {
	try {
		const res = await fetch(`${API_URL}/alarms/status`);
		const data = await res.json();
		return data;
	} catch (err: any) {
		console.error('Fel vid hämtning av alarm status:', err.message);
		throw err;
	}
}

export async function startAlarmMonitoring() {
	try {
		const res = await fetch(`${API_URL}/alarms/monitoring/start`, {
			method: 'POST'
		});
		const data = await res.json();
		return data;
	} catch (err: any) {
		console.error('Fel vid start av alarm monitoring:', err.message);
		throw err;
	}
}

export async function stopAlarmMonitoring() {
	try {
		const res = await fetch(`${API_URL}/alarms/monitoring/stop`, {
			method: 'POST'
		});
		const data = await res.json();
		return data;
	} catch (err: any) {
		console.error('Fel vid stopp av alarm monitoring:', err.message);
		throw err;
	}
}
