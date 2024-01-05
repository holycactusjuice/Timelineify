import { BrowserRouter } from "react-router-dom";

import { About, Navbar, Overview, Timeline } from "./components";

const App = () => {
    return (
        <BrowserRouter>
            <Navbar />
            <Overview />
            <Timeline />
            <About />
        </BrowserRouter>
    );
};

export default App;
