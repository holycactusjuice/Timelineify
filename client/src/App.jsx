import { BrowserRouter } from "react-router-dom";
import React, { useState, useEffect } from "react";

import { MonthProvider } from "./contexts";
import {
    About,
    MonthView,
    Navbar,
    Login,
    Timeline,
    Tracks,
} from "./components";

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        fetch("http://localhost:5000/is-logged-in", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => {
                setIsLoggedIn(data.is_logged_in);
                console.log(data.is_logged_in);
            })
            .catch((error) => console.log(error));
    }, []);

    return (
        <BrowserRouter>
            <div className="relative z-0 bg-primary">
                <Navbar isLoggedIn={isLoggedIn} />
                {isLoggedIn ? (
                    <div class="">
                        <MonthProvider>
                            <Timeline />
                            <MonthView />
                            <Tracks />
                        </MonthProvider>
                    </div>
                ) : (
                    <Login />
                )}

                <About />
            </div>
        </BrowserRouter>
    );
};

export default App;
