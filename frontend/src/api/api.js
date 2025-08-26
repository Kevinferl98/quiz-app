import {fetchAuthSession } from 'aws-amplify/auth';

export async function apiFetch(url, options = {}) {
    const session = await fetchAuthSession();
    const token = session.tokens?.accessToken?.toString();

    const mergedOptions = {
        ...options,
        headers: {
            ...(options.headers || {}),
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    };

    const response = await fetch(url, mergedOptions);
    if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
    }
    return response.json();
}