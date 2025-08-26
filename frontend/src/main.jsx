import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import * as AmplifyLib from "aws-amplify";
import awsconfig from "./aws-exports"

AmplifyLib.Amplify.configure(awsconfig);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>,
);