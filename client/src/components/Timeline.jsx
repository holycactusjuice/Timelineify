import React, { useState, useEffect } from "react";
import {
    VerticalTimeline,
    VerticalTimelineElement,
} from "react-vertical-timeline-component";
import { motion } from "framer-motion";
import "react-vertical-timeline-component/style.min.css";

import { useMonth } from "../contexts";
import { styles } from "../styles";
import { textVariant } from "../utils/motion";
import { downArrow } from "../assets";

const MonthCard = ({ month, monthData }) => {
    const { setMonth } = useMonth();

    const handleMonthChange = (newMonth) => {
        setMonth(newMonth);
    };

    return (
        <VerticalTimelineElement
            contentStyle={{ background: "#222", color: "#eee" }}
            contentArrowStyle={{ borderRight: "7px solid  #232631" }}
            month={month}
            className="vertical-timeline-element--work"
            iconStyle={{
                background: "black",
                color: "#fff",
            }}
            icon={
                <div className="flex justify-center items-center w-full h-full">
                    <img
                        src={monthData[0].album_art_url}
                        alt={monthData[0].title}
                        style={{ borderRadius: "50%" }}
                    />
                </div>
            }
        >
            <div>
                <p
                    className="text-secondary text-[16px] font-semibold"
                    style={{ margin: 0 }}
                >
                    Your top tracks for
                </p>
                <h3 className="text-white text-[24px] font-bold">{month}</h3>
            </div>
            <ol className="mt-5 list-decimal ml-5 space-y-2">
                {monthData ? (
                    monthData.slice(0, 5).map((track) => {
                        return (
                            <li
                                key={track.track_id}
                                className="text-white-100 text-[14px] pl-1 tracking-wider"
                            >
                                {track.title} - {track.artists.join(", ")}
                            </li>
                        );
                    })
                ) : (
                    <div></div>
                )}
            </ol>

            <div className="mt-5 text-[14px] text-secondary hover:underline">
                <a href="#monthview" onClick={() => handleMonthChange(month)}>
                    view stats and tracks
                </a>
            </div>
        </VerticalTimelineElement>
    );
};

const Timeline = () => {
    const [timelineData, setTimelineData] = useState(null);

    useEffect(() => {
        fetch("http://localhost:5000/timeline-data", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setTimelineData(data))
            .catch((error) => console.log(error));
    }, []);

    return (
        <section class="">
            <h2
                className={`${styles.sectionHeadText} text-center pt-[80px]`}
                id="timeline"
            >
                Your Spotify timeline
            </h2>

            <div className="mt-20 flex flex-col">
                <VerticalTimeline>
                    {timelineData ? (
                        <div>
                            {timelineData.map((item) => (
                                <MonthCard
                                    key={item.month}
                                    month={item.month}
                                    monthData={item.data}
                                />
                            ))}
                        </div>
                    ) : (
                        <></>
                    )}
                </VerticalTimeline>
                <div class="flex justify-center mt-[120px]">
                    <a href="#monthview">
                        <img src={downArrow} alt="down arrow" class="h-10" />
                    </a>
                </div>
            </div>
        </section>
    );
};

export default Timeline;
