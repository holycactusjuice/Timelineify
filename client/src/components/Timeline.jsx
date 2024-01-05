import React from "react";
import {
    VerticalTimeline,
    VerticalTimelineElement,
} from "react-vertical-timeline-component";
import { motion } from "framer-motion";

const TimelineCard = ({ data }) => {
    return (
        <VerticalTimelineElement
            className="vertical-timeline-element--work"
            date={data.date}
            iconStyle={{ background: "rgb(33, 150, 243)", color: "#fff" }}
            icon={<i className="fas fa-graduation-cap"></i>}
        >
            <h3 className="vertical-timeline-element-title">{data.title}</h3>
            <h4 className="vertical-timeline-element-subtitle">
                {data.subtitle}
            </h4>
            <p>{data.description}</p>
        </VerticalTimelineElement>
    );
};

const Timeline = () => {
    return (
        <>
            <div className="mt-20 flex flex-col">potato</div>
        </>
    );
};

export default Timeline;
