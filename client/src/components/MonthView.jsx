import React, { useState, useEffect } from "react";

const MonthView = () => {
    const [monthViewData, setMonthViewData] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/monthview-data/01-2024", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setMonthViewData(data))
            .catch((error) => console.log(error));
    }, []);

    return (
        <div>
            {monthViewData ? (
                <div>
                    <div>Last month, you listened to</div>
                    <div>{monthViewData.tracks_count} unique tracks</div>
                    <div>a combined</div>
                    <div>{monthViewData.total_plays} times</div>
                    <div>for a total of</div>
                    <div>
                        {monthViewData.time_listened.hours} hours
                        {monthViewData.time_listened.minutes} minutes
                        {monthViewData.time_listened.seconds} seconds
                    </div>
                </div>
            ) : (
                <div>Loading...</div>
            )}
        </div>
    );
};

export default MonthView;
