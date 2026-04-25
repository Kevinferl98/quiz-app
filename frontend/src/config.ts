const getEnv = (key: string, defaultValue: string): string => {
    return import.meta.env[key] || defaultValue;
};

export const CONFIG = {
    API_BASE: getEnv("VITE_API_BASE_URL", "/api"),
    WS_BASE: getEnv("VITE_WS_BASE_URL", "ws://localhost:8000/ws"),
    
    KEYCLOAK_URL: getEnv("VITE_KEYCLOAK_URL", "http://localhost:8081"),
    KEYCLOAK_REALM: getEnv("VITE_KEYCLOAK_REALM", "quiz"),
    KEYCLOAK_CLIENT_ID: getEnv("VITE_KEYCLOAK_CLIENT_ID", "quiz-frontend")
};