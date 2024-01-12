import React, { useState, useEffect } from "react";

import { useMonth } from "../contexts";
import { styles } from "../styles";
import { downArrow } from "../assets";

const MonthView = () => {
    const { month } = useMonth();

    const [monthViewData, setMonthViewData] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:5000/monthview-data/${month}`, {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setMonthViewData(data))
            .catch((error) => console.log(error));
    }, [month]);

    return (
        <>
            {monthViewData ? (
                <>
                    <div
                        id="monthview"
                        class="flex flex-col items-center justify-center min-h-screen"
                    >
                        <div class="text-center">
                            <h2
                                class={`${styles.sectionSubText} text-center my-6`}
                            >
                                In {month},
                            </h2>
                            <p>you listened to</p>

                            <div class="items-center space-x-2">
                                <p class="text-[60px] font-semibold">
                                    {monthViewData.tracks_count} unique tracks
                                </p>
                            </div>

                            <p>for a combined</p>
                            <div class="items-center space-x-2">
                                <p class="text-[60px] font-semibold">
                                    {monthViewData.total_plays} listens
                                </p>
                            </div>
                            <p>and a total of</p>
                            <div class="items-center space-x-2">
                                <p class="text-[60px] font-semibold">
                                    {monthViewData.time_listened.hours} hours,{" "}
                                    {monthViewData.time_listened.minutes}{" "}
                                    minutes,{" "}
                                    {monthViewData.time_listened.seconds}{" "}
                                    seconds
                                </p>
                            </div>
                        </div>
                        <div class="flex justify-center mt-10">
                            <a href="#tracks">
                                <img
                                    src={downArrow}
                                    alt="down arrow"
                                    class="h-10"
                                />
                            </a>
                        </div>
                    </div>
                </>
            ) : (
                <></>
            )}
        </>
    );
};

export default MonthView;
