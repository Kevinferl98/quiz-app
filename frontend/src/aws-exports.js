const awsconfig = {
    Auth: {
      Cognito: {
        region: process.env.REACT_APP_COGNITO_REGION || "",
        userPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID || "",
        userPoolClientId: process.env.REACT_APP_COGNITO_USER_POOL_CLIENT_ID || "",
        mandatorySignIn: true
      }
    },
}

export default awsconfig;