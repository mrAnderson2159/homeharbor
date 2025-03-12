// frontend/src/App.jsx
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import Header from "./components/Layout/Header/Header";
import Home from "./pages/Home/Home";
import Paperless from "./pages/Paperless/Paperless";

export default function App() {
    // 🎨 Inizializza i tooltip di Bootstrap, serve a creare i popover
    useEffect(() => {
        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );
        tooltipTriggerList.forEach((el) => {
            // eslint-disable-next-line no-undef
            new bootstrap.Tooltip(el, {
                delay: { show: 1000, hide: 100 }, // 1 secondo
            });
        });
    }, []);

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
