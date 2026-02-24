import keycloak from "../auth/keycloak";

export async function apiFetch<T = any>(
    url: string, 
    options: RequestInit = {},
    requireAuth: boolean = false
): Promise<T> {
    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string> || {}),
    };

    if (requireAuth) {
        if (!keycloak.authenticated) {
            throw new Error("User not authenticated");
        }
        await keycloak.updateToken(30);

        headers["Authorization"] = `Bearer ${keycloak.token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
    }
    
    return response.json()
}