import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";

import { useMonth } from "../contexts";
import { styles } from "../styles";
import { textVariant } from "../utils/motion";
import { slideIn } from "../utils/motion";

const Track = ({ track, rank }) => {
    return (
        <div class="text-gray-300 flex items-center grid grid-cols-[50px_100px_280px_110px_130px] gap-x-8 text-left text-lg font-light mt-10 mb-10 h-[100px]">
            <motion.div
                class="text-right"
                variants={slideIn("left", "tween", 0.2, 1)}
            >
                {rank}
            </motion.div>
            <div>
                <img
                    src={track.album_art_url}
                    alt={`album art for ${track.title}`}
                    width="100"
                />
            </div>
            <div>
                <a
                    href={`https://open.spotify.com/track/${track.track_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="hover:text-white hover:underline line-clamp-1"
                >
                    {track.title}
                </a>
                <div class="text-[14px] line-clamp-1">
                    {track.artists.join(", ")}
                </div>
            </div>
            <div class="text-right">{track.plays} plays</div>
            <div class="text-right">
                {Math.floor(track.time_listened / 60)} minutes
            </div>
        </div>
    );
};

const Tracklist = () => {
    const { month } = useMonth();
    const [length, setLength] = useState(-1);
    const [tracks, setTracks] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:5000/tracks/${month}/${length}`, {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => setTracks(data))
            .catch((error) => console.log(error));
    }, [month, length]);

    const notify = () => toast("Playlist added to your library!");

    // create playlist
    const handleClick = () => {
        fetch(`http://localhost:5000//top-tracks-playlist/${month}/${length}`, {
            method: "GET",
            credentials: "include",
        }).catch((error) => console.log(error));
    };

    return (
        <div id="tracks" class="pt-[80px]">
            {tracks.length > 0 ? (
                <>
                    <motion.div variants={textVariant()}>
                        <h2 class={`${styles.sectionHeadText} text-center`}>
                            Your top {length === -1 ? "" : length} tracks for{" "}
                            {month}
                        </h2>
                    </motion.div>
                    <div class="mt-5 text-gray-500">
                        <div
                            class="flex justify-center grid grid-cols-[25px_25px_25px_25px_25px] gap-x-10"
                            style={{
                                marginLeft: "auto",
                                marginRight: "auto",
                            }}
                        >
                            <button
                                onClick={() => setLength(-1)}
                                class={`${
                                    length === -1
                                        ? "text-gray-200 font-semibold"
                                        : ""
                                }`}
                            >
                                All
                            </button>
                            <button
                                onClick={() => setLength(10)}
                                class={`${
                                    length === 10
                                        ? "text-gray-200 font-semibold"
                                        : ""
                                }`}
                            >
                                10
                            </button>
                            <button
                                onClick={() => setLength(25)}
                                class={`${
                                    length === 25
                                        ? "text-gray-200 font-semibold"
                                        : ""
                                }`}
                            >
                                25
                            </button>
                            <button
                                onClick={() => setLength(50)}
                                class={`${
                                    length === 50
                                        ? "text-gray-200 font-semibold"
                                        : ""
                                }`}
                            >
                                50
                            </button>
                            <button
                                onClick={() => setLength(100)}
                                class={`${
                                    length === 100
                                        ? "text-gray-200 font-semibold"
                                        : ""
                                }`}
                            >
                                100
                            </button>
                        </div>
                    </div>
                    <div
                        class="mt-5 justify-center"
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                        }}
                    >
                        <button
                            class={
                                "text-center text-[20px] text-gray-400 hover:text-gray-200 hover:font-semibold"
                            }
                            onClick={() => {
                                notify();
                                handleClick();
                            }}
                        >
                            Add playlist to library
                        </button>
                        <Toaster />
                    </div>
                    <div
                        class="flex justify-center"
                        style={{
                            marginLeft: "auto",
                            marginRight: "auto",
                        }}
                    >
                        <div>
                            {tracks.map((track, index) => (
                                <Track track={track} rank={index + 1} />
                            ))}
                        </div>
                    </div>
                </>
            ) : (
                <div></div>
            )}
        </div>
    );
};

export default Tracklist;
