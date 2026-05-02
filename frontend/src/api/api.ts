import keycloak from "../auth/keycloak";
import { CONFIG } from "../config";

function randomHex(bytes: number): string {
    const arr = new Uint8Array(bytes);
    crypto.getRandomValues(arr);
    return Array.from(arr, (b) => b.toString(16).padStart(2, "0")).join("");
}

function buildTraceparent(): string {
    const version = "00";
    const traceId = randomHex(16);
    const parentId = randomHex(8);
    const flags = "01";
    return `${version}-${traceId}-${parentId}-${flags}`;
}

export async function apiFetch<T = any>(
    endpoint: string, 
    options: RequestInit = {},
    requireAuth: boolean = false
): Promise<T> {
    const fullUrl = `${CONFIG.API_BASE}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string> || {}),
    };
    headers["traceparent"] = buildTraceparent();
    const traceState = (window as Window & { __TRACESTATE__?: string }).__TRACESTATE__;
    if (traceState) {
        headers["tracestate"] = traceState;
    }

    if (requireAuth) {
        if (!keycloak.authenticated) {
            throw new Error("User not authenticated");
        }
        await keycloak.updateToken(30);

        headers["Authorization"] = `Bearer ${keycloak.token}`;
    }

    const response = await fetch(fullUrl, {
        ...options,
        headers
    });

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
    }
    
    return response.json()
}