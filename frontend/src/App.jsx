// src/App.jsx
import { useState, useEffect } from "react";
import axios from "axios";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import { BACKEND_ADDRESS } from "./config.js";
import "./App.css";

export default function App() {
    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Benvenuto in HomeHarbor 🏠</h1>
            <button className="btn btn-primary">Apri</button>
        </div>
    );
}
