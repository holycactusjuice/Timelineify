import React, { useState, useEffect } from "react";

const App = () => {
    const [data, setData] = useState([{}]);

    useEffect(() => {
        fetch("/members") // gets data from /members route from backend
            .then((res) => res.json()) // parse response into json
            .then((data) => {
                setData(data); // set data to json that was received
                console.log(data); // test log
            });
    }, []); //depdendency array here so that useEffect only runs on first rendering

    return (
        <div>
            {typeof data.members == "undefined" ? (
                <p>Loading...</p>
            ) : (
                data.members.map((member, i) => <p key={i}>{member}</p>)
            )}
        </div>
    );
};

export default App;
