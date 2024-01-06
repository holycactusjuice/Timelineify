import React from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const handleLogin = () => {
        // redirect to /login in the backend
        window.location.href = "http://localhost:5000/login";
    };

    return (
        <div>
            <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;
