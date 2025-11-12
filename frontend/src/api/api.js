import {fetchAuthSession } from 'aws-amplify/auth';

const BASE_ECS = process.env.REACT_APP_BASE_ECS || "http://localhost:8080";
const BASE_LAMBDA = process.env.REACT_APP_BASE_LAMBDA || "http://localhost:3001";

export async function apiFetch(path, options = {}, lambda = false) {
    const session = await fetchAuthSession();
    const token = session.tokens?.accessToken?.toString();

    const url = lambda ? `${BASE_LAMBDA}${path}` : `${BASE_ECS}${path}`;

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