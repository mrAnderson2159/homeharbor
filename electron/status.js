// electron/status.js

/**
 * Stato globale condiviso tra i moduli principali di Electron.
 *
 * Questo oggetto viene utilizzato per:
 * - tracciare lo stato di esecuzione di ciascun componente (DB, backend, frontend, UI);
 * - conservare i riferimenti ai processi avviati;
 * - salvare le informazioni dinamiche durante l'esecuzione (porte, URL, PID, ecc.).
 *
 * ⚠️ È una struttura centrale nel coordinamento tra moduli e va aggiornata in modo coerente.
 */

const status = {
    // ✅ Indica se il database è attualmente in esecuzione
    databaseRunning: false,

    // ✅ Indica se il backend (FastAPI/Uvicorn) è avviato correttamente
    backendRunning: false,

    // ✅ Indica se il frontend (React/Vite) è in esecuzione
    frontendRunning: false,

    // ✅ Indica se la finestra principale di Electron è aperta
    mainWindowRunning: false,

    // 🔁 PID del processo "reloader" di Uvicorn (gestisce il reload live)
    reloaderPid: null,

    // 🔁 PID del server Uvicorn principale
    serverPid: null,

    // 🛠 Modalità debug attiva (true se DEBUG_MODE === "true")
    debugMode: false,

    // 🗃️ Nome del database attualmente attivo (es. "homeharbor")
    databaseName: null,

    // 🧠 Riferimento diretto al processo del backend (per terminazione manuale)
    backendProcess: null,

    // 🌐 Indirizzo HTTP su cui il backend è accessibile (es. http://localhost:18000)
    backendAddress: null,

    // 🌍 Indirizzo HTTP su cui il frontend è accessibile (es. http://localhost:15713)
    frontendAddress: null,

    // 🖥️ Riferimento alla finestra principale di Electron (BrowserWindow)
    mainWindow: null,
};

module.exports = status;
