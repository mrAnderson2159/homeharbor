// electron/main.js
const { log, error } = console;
const { app } = require("electron");

// 🔌 Inizializza gli handler IPC
require("./ipc");

const { openApp } = require("./lifecycle/openApp");
const { quitApp } = require("./lifecycle/quitApp");
const { listenForQuitCmd } = require("./lifecycle/listenQuitCmd");

/* ---------------------------------- Avvio dell'app ---------------------------------- */
// Disabilita la funzionalità di autocompletamento di Chrome per evitare un fastidioso
// warning di sicurezza quando si apre la DevTools
app.commandLine.appendSwitch("disable-features", "Autofill");

app.whenReady().then(async () => {
    listenForQuitCmd(); // 🔥 Ascolta i comandi di chiusura manuali
    try {
        await openApp();
    } catch (err) {
        error(err);
        await quitApp();
    }
});

/* ---------------------------------- Gestione degli eventi ---------------------------------- */
app.on("window-all-closed", async () => {
    log("🛑 Tutte le finestre sono state chiuse...");
    await quitApp();
});
