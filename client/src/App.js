import React, { useState, useEffect } from "react";

const App = () => {
    const [data, setData] = useState([{}]);

    useEffect(() => {
        fetch("/") // gets data from /members route from backend
            .then((res) => res.json()) // parse response into json
            .then((data) => {
                setData(data); // set data to json that was received
                console.log(data); // test log
            });
    }, []); //depdendency array here so that useEffect only runs on first rendering

    return (
        // button to test spotify login route from backend
        <div>
            <a href="http://localhost:5000/login">Login to Spotify</a>
        </div>
    );
};

export default App;
