import React from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const handleLogin = () => {
        // redirect to /auth/login in the backend
        fetch("http://localhost:5000/login").then((res) => {
            console.log(res);
        });
    };

    return (
        <div>
            <button onClick={handleLogin}>Login</button>
        </div>
    );
};

export default Login;
