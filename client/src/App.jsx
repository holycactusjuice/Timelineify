import { BrowserRouter } from "react-router-dom";

import { About, Login, Navbar, Overview, Timeline } from "./components";

const App = () => {
    return (
        <BrowserRouter>
            <Navbar />
            <Login />
            <Overview />
            <Timeline />
            <About />
        </BrowserRouter>
    );
};

export default App;
