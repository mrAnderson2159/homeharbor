// electron/services/backend.js

/**
 * Modulo per la gestione del backend (FastAPI/Uvicorn) di HomeHarbor.
 *
 * Questo modulo fornisce due funzioni:
 * - `startBackend()`: avvia il server backend su una porta definita;
 * - `quitBackend()`: arresta completamente il backend, inclusi i processi di reload e server.
 *
 * Il backend viene eseguito tramite `uvicorn` e supporta modalità di debug, variabili d'ambiente,
 * e configurazioni dinamiche derivate da `status` e `constants`.
 */

const { log, error } = require("console");
const { spawn, exec } = require("child_process");
const CONSTANTS = require("../constants");
const status = require("../status");

/**
 * Avvia il backend FastAPI tramite `uvicorn`, impostando dinamicamente
 * le variabili d’ambiente per collegamento a frontend, database e debug mode.
 *
 * Durante l’avvio, cattura stdout e stderr per:
 * - registrare PID di reloader/server;
 * - determinare se il backend è correttamente avviato;
 * - ottenere l’indirizzo su cui è disponibile.
 *
 * @returns {Promise<ChildProcess>} - Il processo backend attivo, utile per kill o logging
 */
function startBackend() {
    return new Promise((resolve, reject) => {
        log("\n🚀 Avvio del backend in corso...");

        const backendProcess = spawn(
            "uvicorn",
            ["app.main:app", "--reload", "--port", CONSTANTS.BACKEND_PORT],
            {
                cwd: "backend", // 📁 Usa la directory del backend come working dir
                env: {
                    ...process.env,
                    VIRTUAL_ENV: "venv/bin/activate",
                    FRONTEND_ADDRESS: `${CONSTANTS.HOST}:${CONSTANTS.FRONTEND_PORT}`,
                    DEBUG_MODE: status.debugMode ? "true" : "false",
                    DATABASE: status.databaseName,
                    DATABASE_PORT: CONSTANTS.DATABASE_PORT,
                },
                shell: true, // 🐚 Necessario per usare comandi zsh/bash da spawn
            }
        );

        // 🔍 Monitoraggio dell’output in tempo reale per tracciare avvio e PID
        backendProcess.stdout.on("data", (data) => {
            log(data.toString());
        });

        backendProcess.stderr.on("data", (data) => {
            data = data.toString();

            // ✅ Uvicorn ha avviato il server: estraiamo l'indirizzo
            if (data.includes("Uvicorn running on")) {
                status.backendAddress = data
                    .match(/(http:\/\/[0-9a-zA-Z.\/-:]+)/i)[1]
                    .replace("127.0.0.1", "localhost");

                log(`🚀 Backend avviato su ${status.backendAddress}`);

                // 🔁 Estrae il PID del processo "reloader" (usato per hot-reload)
                status.reloaderPid = data.match(/\[(\d+)\]/i)[1];
                log(
                    `🔄 Processo di ricarica backend avviato con PID ${status.reloaderPid}`
                );

                // ✅ Rileva il PID del processo server vero e proprio
            } else if (data.includes("Started server process")) {
                status.serverPid = data.match(/\[(\d+)\]/i)[1];
                log(`🔄 Backend server avviato con PID ${status.serverPid}`);

                // ✅ Uvicorn ha completato l'avvio → risolviamo la promise
            } else if (data.includes("Application startup complete")) {
                resolve(backendProcess);
                log(`✅ Backend avviato correttamente`);

                // ❌ Uvicorn ha lanciato un errore critico
            } else if (data.includes("Error")) {
                reject(data);

                // 📃 Altri log normali
            } else {
                log(data);
            }
        });

        // 🛑 Monitoriamo la chiusura del backend
        backendProcess.on("exit", (code) => {
            if (code !== null) log(`🔴 Backend terminato con codice ${code}`);
        });
    });
}

/**
 * Arresta il backend in modo completo, terminando sia il processo di ricarica
 * (`--reload`) che il processo server Uvicorn.
 *
 * Utilizza `kill -9` con i PID tracciati precedentemente.
 *
 * @returns {Promise<void>}
 */
function quitBackend() {
    return new Promise((resolve, reject) => {
        log("🛑 Arresto del backend in corso...");
        exec(`kill -9 ${status.reloaderPid} ${status.serverPid}`, (err) => {
            if (!err) {
                log(`✅ Backend arrestato correttamente`);
                resolve();
            } else {
                error(`❌ Errore durante l'arresto del backend: ${err}`);
                reject(err);
            }
        });
    });
}

// ✅ Esportazione delle funzioni per utilizzo esterno
module.exports = {
    startBackend,
    quitBackend,
};
