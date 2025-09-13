import { useNavigate } from "react-router-dom";
import { Authenticator } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";

export default function HomePage() {
  const navigate = useNavigate();

  const components = {
    SignIn: {
      Footer() {
        return null;
      },
      ForgotPasswordLink() {
        return null;
      }
    },
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
      <Authenticator hideSignUp components={components}>
        {({ user }) => {
          if (user) navigate("/quizzes");
          return null;
        }}
      </Authenticator>
    </div>
  );
}
