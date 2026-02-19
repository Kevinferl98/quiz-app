export async function apiFetch<T = any>(url: string, options: RequestInit = {}): Promise<T> {
    const mergedOptions: RequestInit = {
        ...options,
        headers: {
            ...(options.headers || {}),
            "Content-Type": "application/json",
        },
    };

    const response = await fetch(url, mergedOptions);
    if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
    }
    return response.json()
}