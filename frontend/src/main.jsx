// frontend/src/main.jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";

// 🎨 Importa lo stile base e Bootstrap
import "./index.scss";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./styles/theme.scss";
import "bootstrap-icons/font/bootstrap-icons.css";

// 🧠 Importa il contesto tema
import { ThemeProvider } from "./context/ThemeContext";

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <ThemeProvider>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </ThemeProvider>
    </StrictMode>
);
