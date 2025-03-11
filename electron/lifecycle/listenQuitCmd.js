// electron/lifecycle/listenQuitCmd.js

/**
 * Modulo per la gestione della chiusura manuale dell'applicazione
 * tramite comando da terminale (digitazione della lettera `q`).
 *
 * Questa funzionalità è pensata per ambienti di sviluppo o testing
 * in cui l'app viene eseguita da console e si desidera un modo rapido
 * e controllato per arrestarla senza chiudere la finestra.
 *
 * Il modulo:
 * - imposta l'input `stdin` per ascoltare comandi da tastiera;
 * - attende la pressione del tasto `q` seguita da invio (`Enter`);
 * - richiama la funzione `quitApp()` per eseguire la sequenza completa di arresto.
 */

const { log } = console;
const { stdin } = process;
const { quitApp } = require("./quitApp");

/**
 * Attiva l'ascolto da terminale per il comando `q`.
 *
 * Quando viene ricevuto, si avvia la procedura di chiusura
 * dell'applicazione (`quitApp()`), includendo arresto servizi
 * e uscita da Electron.
 */
function listenForQuitCmd() {
    stdin.setEncoding("utf-8"); // 🎙️ Permette di leggere input testuali da terminale

    log("🔵 Digita 'q' e premi Invio per chiudere l'app in sicurezza\n");

    // 🧠 Ascolta ogni input inserito da tastiera
    stdin.on("data", (data) => {
        if (data.trim() === "q") {
            log("🛑 Ricevuto comando di chiusura manuale...");
            quitApp(); // 🔥 Attiva il flusso di chiusura normale
        }
    });

    stdin.resume(); // ⏳ Mantiene la console attiva in attesa di input
}

module.exports = { listenForQuitCmd };
