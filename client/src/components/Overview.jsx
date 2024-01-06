import React, { useState, useEffect } from "react";

const Overview = () => {
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
        <div>
            <h1>Overview</h1>
            {/* Render user data */}
            {userData && (
                <div>
                    <p>User ID: {userData.user_id}</p>
                    <p>Email: {userData.email}</p>
                    {/* Add more user data fields */}
                </div>
            )}
        </div>
    );
};

export default Overview;
