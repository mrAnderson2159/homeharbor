// frontend/src/App.jsx
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Layout/Header/Header";
import Home from "./pages/Home/Home";
import Paperless from "./pages/Paperless/Paperless";

export default function App() {
    return (
        <>
            <Header />
            <main id="main">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/paperless" element={<Paperless />} />
                </Routes>
            </main>
        </>
    );
}
