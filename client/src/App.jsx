import { BrowserRouter } from "react-router-dom";

import { About, MonthView, Navbar, Overview, Timeline } from "./components";

const App = () => {
    return (
        <BrowserRouter>
            <Navbar />
            <Overview />
            <Timeline />
            <MonthView />
            <About />
        </BrowserRouter>
    );
};

export default App;
