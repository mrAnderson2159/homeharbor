// electron/lifecycle/openApp.js

/**
 * Entry point per l'avvio dell'applicazione HomeHarbor.
 *
 * Questo modulo esegue l'intera sequenza di avvio:
 * - Legge e interpreta le variabili d'ambiente (`processEnv`);
 * - Avvia il database locale PostgreSQL (`startDatabase`);
 * - Avvia il backend Python (FastAPI/Uvicorn) (`startBackend`);
 * - Avvia il frontend React/Vite (`startFrontend`);
 * - Apre la finestra principale Electron (`createWindow("main")`).
 *
 * Ogni servizio aggiornando lo stato globale (`status.js`) per tenere traccia
 * dell'esecuzione e dei riferimenti ai processi e finestre attivi.
 */

const { log } = console;
const { startDatabase } = require("../services/database");
const { startBackend } = require("../services/backend");
const { startFrontend } = require("../services/frontend");
const { createWindow } = require("../services/window");
const status = require("../status");

/**
 * Analizza le variabili d'ambiente disponibili e aggiorna `status`.
 * - DEBUG_MODE: true/false → imposta lo stato `debugMode`
 * - DATABASE: nome del database da usare (default: "homeharbor")
 */
function processEnv() {
    const env = { ...process.env };

    if (env.DEBUG_MODE === "true") {
        status.debugMode = true;
        log("🟢 Avvio in modalità DEBUG");
    } else {
        log("⚪ Avvio in modalità normale");
    }

    status.databaseName = env.DATABASE || "homeharbor";
    log(`🔢 Nome database: ${status.databaseName}`);

    log(); // Linea vuota per leggibilità
}

/**
 * Avvia l'intera applicazione HomeHarbor in sequenza.
 *
 * - Avvia il database e aggiorna `status.databaseRunning`
 * - Avvia il backend, salva il processo e l'indirizzo in `status`
 * - Avvia il frontend, salva il processo e l'indirizzo in `status`
 * - Apre la finestra principale (`createWindow("main")`)
 */
async function openApp() {
    processEnv();

    // 🔹 Avvio del database
    const db_port = await startDatabase();
    status.databaseRunning = true;

    // 🔹 Avvio del backend
    const backendProcess = await startBackend();
    status.backendRunning = true;
    status.backendProcess = backendProcess;

    // 🔹 Avvio del frontend
    const frontendProcess = await startFrontend();
    status.frontendRunning = true;
    status.frontendProcess = frontendProcess;

    // 🖼️ Apertura finestra principale
    createWindow("main");
    status.mainWindowRunning = true;
}

module.exports = { openApp };
