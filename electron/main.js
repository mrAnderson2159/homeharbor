// electron/main.js
const { app, BrowserWindow, ipcMain } = require("electron");
const { exec, spawn } = require("child_process");
const { log } = require("console");
const path = require("path");
const settings = require("./settings");

const CONSTANTS = {
    DATABASE_PORT: 15432,
    BACKEND_PORT: 18000,
    FRONTEND_PORT: 15713,
};

const status = {
    databaseRunning: false,
    backendRunning: false,
    frontendRunning: false,
    mainWindowRunning: false,
    reloaderPid: null,
    serverPid: null,
    debugMode: false,
    backendProcess: null,
    backendAddress: null,
    frontendAddress: null,
    host: "http://localhost",
};

let mainWindow;

/* ---------------------------------- Funzioni database ---------------------------------- */

function startDatabase() {
    return new Promise((resolve, reject) => {
        function attemptStart(port) {
            exec(
                `pg_ctl -D ./database -l ./database/postgresql.log start -o "-p ${port}"`,
                (err, stdout, stderr) => {
                    if (!err) {
                        console.log(
                            `✅ Database avviato correttamente sulla porta ${port}`
                        );
                        resolve(port);
                        return;
                    }

                    if (
                        [
                            "un altro server",
                            "l'avvio del server è fallito",
                        ].some((e) => stderr.toString().includes(e))
                    ) {
                        console.log(
                            `❗️ Database già avviato sulla porta ${port},`,
                            `controllo la presenza del database homeharbor...`
                        );

                        exec(
                            `psql -p ${port} -c "SELECT 1" homeharbor`,
                            (err, stdout, stderr) => {
                                if (!err) {
                                    console.log(
                                        `✅ Database homeharbor trovato sulla porta ${port}`
                                    );
                                    resolve(port);
                                    return;
                                } else {
                                    const newPort =
                                        Math.floor(Math.random() * 10000) +
                                        9999;
                                    console.log(`❌ Database homeharbor non trovato sulla porta ${port}, 
                                provo ad avviarlo sulla porta ${newPort}`);

                                    attemptStart(newPort);
                                }
                            }
                        );
                    } else {
                        console.error(
                            `❌ Errore durante l'avvio del database: ${stderr}`
                        );
                        reject(stderr);
                    }
                }
            );
        }

        console.log("🚀 Avvio del database in corso...");
        attemptStart(CONSTANTS.DATABASE_PORT);
    });
}

function quitDatabase() {
    return new Promise((resolve, reject) => {
        log("🛑 Arresto del database in corso...");
        exec(`pg_ctl -D ./database stop`, (err, stdout, stderr) => {
            if (!err) {
                console.log(`✅ Database arrestato correttamente`);
                resolve();
            } else {
                console.error(
                    `❌ Errore durante l'arresto del database: ${stderr}`
                );
                reject(stderr);
            }
        });
    });
}

/* ---------------------------------- Funzioni di backend ---------------------------------- */
function startBackend() {
    return new Promise((resolve, reject) => {
        console.log("\n🚀 Avvio del backend in corso...");

        const backendProcess = spawn(
            "uvicorn",
            ["app.main:app", "--reload", "--port", CONSTANTS.BACKEND_PORT],
            {
                cwd: "backend", // 🔥 Cambiamo la working directory direttamente!
                env: {
                    ...process.env,
                    VIRTUAL_ENV: "venv/bin/activate",
                    FRONTEND_ADDRESS: `${status.host}:${CONSTANTS.FRONTEND_PORT}`,
                    DEBUG_MODE: status.debugMode ? "true" : "false", // 🔥 Aggiungiamo la variabile d'ambiente
                },
                shell: true, // 🔥 Permette a spawn di eseguire comandi shell come in una bash/zsh
            }
        );

        backendProcess.stdout.on("data", (data) => {
            console.log(data.toString());
        });

        backendProcess.stderr.on("data", (data) => {
            data = data.toString();
            if (data.includes("Uvicorn running on")) {
                status.backendAddress = data
                    .match(/(http:\/\/[0-9a-zA-Z.\/-:]+)/i)[1]
                    .replace("127.0.0.1", "localhost");
                console.log(`🚀 Backend avviato su ${status.backendAddress}`);

                status.reloaderPid = data.match(/\[(\d+)\]/i)[1];
                console.log(
                    `🔄 Processo di ricarica backend avviato con PID ${status.reloaderPid}`
                );
            } else if (data.includes("Started server process")) {
                status.serverPid = data.match(/\[(\d+)\]/i)[1];
                console.log(
                    `🔄 Backend server avviato con PID ${status.serverPid}`
                );
            } else if (data.includes("Application startup complete")) {
                resolve(backendProcess);
                console.log(`✅ Backend avviato correttamente`);
            } else if (data.includes("Error")) {
                reject(data);
            } else {
                console.log(data);
            }

            // console.log({ data, status });
        });

        backendProcess.on("exit", (code) => {
            if (code !== null)
                console.log(`🔴 Backend terminato con codice ${code}`);
        });
    });
}

function quitBackend() {
    return new Promise((resolve, reject) => {
        console.log("🛑 Arresto del backend in corso...");
        exec(`kill -9 ${status.reloaderPid} ${status.serverPid}`, (err) => {
            if (!err) {
                console.log(`✅ Backend arrestato correttamente`);
                resolve();
            } else {
                console.error(
                    `❌ Errore durante l'arresto del backend: ${err}`
                );
                reject(err);
            }
        });
    });
}

/* ---------------------------------- Funzioni di frontend ---------------------------------- */
function startFrontend() {
    return new Promise((resolve, reject) => {
        console.log("\n🚀Avvio del frontend in corso...");

        const frontendProcess = spawn(
            "npm",
            ["run", "dev", "--", "--port", CONSTANTS.FRONTEND_PORT],
            {
                cwd: "frontend",
                env: {
                    ...process.env,
                    VITE_DEBUG_MODE: status.debugMode ? "true" : "false", // 🔥 Aggiungiamo la variabile d'ambiente
                    VITE_BACKEND_ADDRESS: `${status.host}:${CONSTANTS.BACKEND_PORT}`,
                },
                shell: true,
            }
        );

        frontendProcess.stdout.on("data", (data) => {
            data = data.toString();
            if (data.includes("http")) {
                status.frontendAddress = data.match(
                    /(http:\/\/[0-9a-zA-Z.\/-:]+)/i
                )[1];
                console.log(`🔄 Frontend avviato su ${status.frontendAddress}`);
                resolve(frontendProcess);
            }
        });

        frontendProcess.stderr.on("data", (data) => {
            data = data.toString();
            if (data.includes("Error")) {
                reject(data);
            }
        });

        frontendProcess.on("exit", (code) => {
            if (code !== null)
                console.log(`🔴 Frontend terminato con codice ${code}`);
        });
    });
}

function quitFrontend() {
    return new Promise((resolve, reject) => {
        console.log("🛑 Arresto del frontend in corso...");
        try {
            status.frontendProcess.kill("SIGINT");
            console.log("✅ Frontend arrestato correttamente");
            resolve();
        } catch (error) {
            console.error(`❌ Errore durante l'arresto del frontend: ${error}`);
            reject(error);
        }
    });
}

/* ---------------------------------- Funzioni finestra ---------------------------------- */
function loadWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"), // Sicurezza
            nodeIntegration: false,
            contextIsolation: true,
        },
    });

    console.log(
        `🚀 Carico la finestra principale su ${status.frontendAddress}`
    );
    mainWindow.loadURL(status.frontendAddress);

    mainWindow.on("closed", () => {
        mainWindow = null;
    });
}

/* ---------------------------------- Funzioni di apertura ---------------------------------- */
async function openApp() {
    if (process.env.DEBUG_MODE === "true") {
        status.debugMode = true;
        console.log("🟢 Modalità DEBUG attivata!\n");
    } else {
        console.log("⚪ Modalità normale\n");
    }

    const db_port = await startDatabase();
    status.databaseRunning = true;

    const backendProcess = await startBackend();
    status.backendRunning = true;
    status.backendProcess = backendProcess;

    const frontendProcess = await startFrontend();
    status.frontendRunning = true;
    status.frontendProcess = frontendProcess;

    loadWindow();
    status.mainWindowRunning = true;

    // console.log({
    //     frontendAddress: status.frontendAddress,
    //     backendAddress: status.backendAddress,
    // });

    // 🔥 Aggiungiamo il Content Security Policy alla finestra principale come richiesto da electron
    mainWindow.webContents.session.webRequest.onHeadersReceived(
        (details, callback) => {
            callback({
                responseHeaders: {
                    ...details.responseHeaders,
                    "Content-Security-Policy": [
                        `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' ${status.backendAddress} ${status.frontendAddress};`,
                    ],
                },
            });
        }
    );
}

/* ---------------------------------- Funzioni di chiusura ---------------------------------- */
async function quit() {
    await quitDatabase(); // 🔥 Chiudiamo PostgreSQL prima di uscire
    await quitBackend(); // 🔥 Chiudiamo il backend
    await quitFrontend(); // 🔥 Chiudiamo il frontend
    app.quit(); // 🔥 Esce completamente dall'app
}

function listenForQuitCommand() {
    process.stdin.setEncoding("utf-8"); // Imposta l'encoding per leggere input
    console.log(
        "🔵 Digita 'q' e premi Invio per chiudere l'app in sicurezza\n"
    );

    process.stdin.on("data", (data) => {
        if (data.trim() === "q") {
            console.log("🛑 Ricevuto comando di chiusura manuale...");
            quit(); // 🔥 Attiva il flusso di chiusura normale
        }
    });

    process.stdin.resume(); // 🔥 Mantieni aperta la console per ricevere input
}

/* ---------------------------------- Avvio dell'app ---------------------------------- */
// Disabilita la funzionalità di autocompletamento di Chrome per evitare un fastidioso
// warning di sicurezza quando si apre la DevTools
app.commandLine.appendSwitch("disable-features", "Autofill");

app.whenReady().then(async () => {
    listenForQuitCommand(); // 🔥 Ascolta i comandi di chiusura manuali
    try {
        await openApp();
    } catch (err) {
        console.error(err);
        await quit();
    }
});

/* ---------------------------------- Gestione degli eventi ---------------------------------- */
app.on("window-all-closed", async () => {
    console.log("🛑 Tutte le finestre sono state chiuse...");
    await quit();
});

/* ---------------------------------- IPC ---------------------------------- */
ipcMain.handle("settings:get", (event, key) => {
    return settings.get(key);
});

ipcMain.handle("settings:set", (event, key, value) => {
    settings.set(key, value);
});
