const awsconfig = {
    Auth: {
      Cognito: {
        region: "",
        userPoolId: "",
        userPoolClientId: "",
        authenticationFlowType: "USER_PASSWORD_AUTH"
      }
    },
}

export default awsconfig;