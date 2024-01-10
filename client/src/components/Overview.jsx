import React, { useState, useEffect } from "react";
import {
    VerticalTimeline,
    VerticalTimelineElement,
} from "react-vertical-timeline-component";

const Overview = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/user-data", {
            method: "GET",
            // Send the user's cookie along with the request (VERY IMPORTANT)
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setUser(data))
            .catch((error) => console.log(error));
    }, []);

    return (
        <>
            <h1>Overview</h1>
            {/* Render user data */}
            {user && (
                <div>
                    <div>{user.display_name}</div>
                </div>
            )}
            <div></div>
        </>
    );
};

export default Overview;
