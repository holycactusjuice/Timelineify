import React, { createContext, useState, useContext } from "react";

const MonthContext = createContext();

export const useMonth = () => useContext(MonthContext);

export const MonthProvider = ({ children }) => {
    const [month, setMonth] = useState("01-2024");

    return (
        <MonthContext.Provider value={{ month, setMonth }}>
            {children}
        </MonthContext.Provider>
    );
};
