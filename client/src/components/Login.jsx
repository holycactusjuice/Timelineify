import React, { useState, useEffect } from "react";

const Login = ({ isLoggedIn }) => {
    return (
        <div class="h-screen flex justify-center items-center">
            <div>
                <a
                    href="http://localhost:5000/login"
                    class="text-[40px] hover:font-semibold"
                >
                    login with Spotify
                </a>
            </div>
        </div>
    );
};

export default Login;
