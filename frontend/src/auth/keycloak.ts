import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
    url: "http://localhost:8081",
    realm: "quiz",
    clientId: "quiz-frontend"
});

export default keycloak;