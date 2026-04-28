import Keycloak from "keycloak-js";
import { CONFIG } from "../config";

const keycloak = new Keycloak({
    url: CONFIG.KEYCLOAK_URL,
    realm: CONFIG.KEYCLOAK_REALM,
    clientId: CONFIG.KEYCLOAK_CLIENT_ID
});

export default keycloak;