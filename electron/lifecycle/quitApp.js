// electron/lifecycle/quit.js

/**
 * Modulo per la chiusura ordinata dell'applicazione HomeHarbor.
 *
 * Questo modulo si occupa di:
 * - Arrestare il database locale (PostgreSQL);
 * - Arrestare il backend Python (Uvicorn);
 * - Arrestare il frontend React/Vite;
 * - Chiudere l'app Electron.
 *
 * È pensato per essere richiamato:
 * - Quando tutte le finestre vengono chiuse (`app.on("window-all-closed")`);
 * - Quando viene digitata la lettera `q` da terminale (`listenForQuitCmd`);
 * - Quando l'avvio fallisce (`catch` in `main.js`).
 */

const { log, error } = console;
const { app } = require("electron");
const { quitDatabase } = require("../services/database");
const { quitBackend } = require("../services/backend");
const { quitFrontend } = require("../services/frontend");

/**
 * Arresta in modo sicuro tutti i processi avviati e chiude l'app.
 * Ogni funzione chiamata restituisce una `Promise`.
 */
async function quitApp() {
    log("🧨 Avvio della sequenza di chiusura...");

    try {
        await quitDatabase(); // 🔥 Chiude il database PostgreSQL
    } catch (err) {
        error("⚠️ Errore nella chiusura del database (ignorato):", err);
    }

    try {
        await quitBackend(); // 🔥 Chiude il backend (Uvicorn)
    } catch (err) {
        error("⚠️ Errore nella chiusura del backend (ignorato):", err);
    }

    try {
        await quitFrontend(); // 🔥 Chiude il frontend (React/Vite)
    } catch (err) {
        error("⚠️ Errore nella chiusura del frontend (ignorato):", err);
    }

    log("🏁 Uscita completa dall'app.");
    app.quit(); // 🔚 Chiude l'intera app Electron
}

module.exports = { quitApp };
