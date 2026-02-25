import { createContext, useEffect, useState } from "react";
import keycloak from "./keycloak";

interface AuthContextType {
    keycloak: typeof keycloak;
    authenticated: boolean;
}

export const AuthContext = createContext<AuthContextType>({
    keycloak,
    authenticated: false
})

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        keycloak.init({
            onLoad: "check-sso",
            pkceMethod: "S256",
            checkLoginIframe: false,
            redirectUri: "http://localhost:8080/"
        })
        .then((auth) => {
            setAuthenticated(auth);
        })
        .catch((err) => {
            console.error("Keycloak init error:", err);
        });
    }, []);

    return (
        <AuthContext.Provider value={{ keycloak, authenticated }}>
            {children}
        </AuthContext.Provider>
    );
}