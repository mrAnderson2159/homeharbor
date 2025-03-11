// electron/services/frontend.js

/**
 * Modulo per la gestione del frontend (React + Vite) dell'applicazione HomeHarbor.
 *
 * Questo modulo fornisce due funzioni principali:
 * - `startFrontend()`: avvia il frontend React/Vite su una porta configurata;
 * - `quitFrontend()`: arresta in sicurezza il processo del frontend.
 *
 * Durante l’avvio, vengono passate variabili d’ambiente che permettono al frontend di
 * conoscere l'indirizzo del backend e se è in modalità debug.
 */

const { log, error } = console;
const { spawn } = require("child_process");
const CONSTANTS = require("../constants");
const status = require("../status");

/**
 * Avvia il frontend React tramite `npm run dev`, sulla porta specificata in `constants.js`.
 * Il processo viene gestito tramite `spawn`, con shell attiva.
 * Imposta due variabili d’ambiente visibili nel codice Vite:
 * - `VITE_DEBUG_MODE`: true/false a seconda del contesto
 * - `VITE_BACKEND_ADDRESS`: usato dal frontend per contattare il backend
 *
 * @returns {Promise<ChildProcess>} - Il processo avviato, utile per successiva terminazione
 */
function startFrontend() {
    return new Promise((resolve, reject) => {
        log("\n🚀 Avvio del frontend in corso...");

        const frontendProcess = spawn(
            "npm",
            ["run", "dev", "--", "--port", CONSTANTS.FRONTEND_PORT],
            {
                cwd: "frontend", // 📁 Directory in cui eseguire il comando
                env: {
                    ...process.env,
                    VITE_DEBUG_MODE: status.debugMode ? "true" : "false",
                    VITE_BACKEND_ADDRESS: `${CONSTANTS.HOST}:${CONSTANTS.BACKEND_PORT}`,
                },
                shell: true, // 🐚 Necessario per usare comandi shell standard
            }
        );

        // 🔍 Cattura l'output di stdout per determinare l'URL su cui gira il frontend
        frontendProcess.stdout.on("data", (data) => {
            data = data.toString();

            if (data.includes("http")) {
                status.frontendAddress = data.match(
                    /(http:\/\/[0-9a-zA-Z.\/-:]+)/i
                )[1];
                log(`🔄 Frontend avviato su ${status.frontendAddress}`);
                resolve(frontendProcess); // ✅ Avvio riuscito
            }
        });

        // ❌ Cattura eventuali errori da stderr
        frontendProcess.stderr.on("data", (data) => {
            data = data.toString();
            if (data.includes("Error")) {
                reject(data);
            }
        });

        // 🛑 Log alla chiusura del processo frontend
        frontendProcess.on("exit", (code) => {
            if (code !== null) log(`🔴 Frontend terminato con codice ${code}`);
        });
    });
}

/**
 * Arresta il frontend inviando un segnale `SIGINT` al processo React/Vite.
 * Il processo viene salvato in `status.frontendProcess` al momento dell'avvio.
 *
 * @returns {Promise<void>}
 */
function quitFrontend() {
    return new Promise((resolve, reject) => {
        log("🛑 Arresto del frontend in corso...");
        try {
            status.frontendProcess.kill("SIGINT"); // ✅ Interrompe il processo
            log("✅ Frontend arrestato correttamente");
            resolve();
        } catch (e) {
            error(`❌ Errore durante l'arresto del frontend: ${e}`);
            reject(error);
        }
    });
}

// ✅ Esportazione delle funzioni per utilizzo in fase di avvio/chiusura dell'app
module.exports = {
    startFrontend,
    quitFrontend,
};
