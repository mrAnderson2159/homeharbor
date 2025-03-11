// electron/services/window.js

/**
 * Modulo per la creazione e gestione delle finestre Electron.
 *
 * Fornisce una funzione `createWindow()` che può essere usata
 * per aprire la finestra principale o altre finestre secondarie,
 * con gestione flessibile della route e delle opzioni.
 */

const { log } = console;
const { BrowserWindow } = require("electron");
const path = require("path");
const status = require("../status");

/**
 * Crea una nuova finestra Electron, associata a un nome logico.
 *
 * Al momento supporta solo la finestra "main", ma può essere
 * esteso per altri tipi in futuro (es. impostazioni, popup, ecc.).
 *
 * @param {string} name - Nome della finestra logica (es. "main")
 * @param {object} options - Opzioni aggiuntive (es. route, width, height, etc.)
 */
function createWindow(name, options = {}) {
    if (name === "main") {
        status.mainWindow = new BrowserWindow({
            width: options.width || 1200,
            height: options.height || 800,
            webPreferences: {
                preload: path.join(__dirname, "../preload.js"),
                nodeIntegration: false,
                contextIsolation: true,
            },
        });

        log(`🚀 Carico la finestra principale su ${status.frontendAddress}`);
        status.mainWindow.loadURL(status.frontendAddress);

        status.mainWindow.on("closed", () => {
            status.mainWindow = null;
            status.mainWindowRunning = false;
        });

        status.mainWindowRunning = true;

        // 🔒 Imposta una Content Security Policy
        status.mainWindow.webContents.session.webRequest.onHeadersReceived(
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

    // 🚧 In futuro: potremmo gestire finestre diverse qui (es. impostazioni, modali, ecc.)
}

module.exports = {
    createWindow,
};
