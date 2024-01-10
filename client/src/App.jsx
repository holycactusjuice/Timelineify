import { BrowserRouter } from "react-router-dom";
import React, { useState, useEffect } from "react";

import { About, MonthView, Navbar, Overview, Timeline } from "./components";

const App = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/user-data", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setUserData(data))
            .catch((error) => console.log(error));
    }, []);

    return (
        <BrowserRouter>
            <div className="relative z-0 bg-primary">
                <Navbar />
                <Overview />
                <Timeline />
                {/* <MonthView /> */}
                <About />
            </div>
        </BrowserRouter>
    );
};

export default App;
