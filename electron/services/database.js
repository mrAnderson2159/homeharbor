// electron/services/database.js

/**
 * Modulo per la gestione del database PostgreSQL utilizzato da HomeHarbor.
 *
 * Contiene due funzioni principali:
 * - `startDatabase()`: avvia il database sulla porta predefinita, oppure trova una porta libera alternativa;
 * - `quitDatabase()`: arresta il database.
 *
 * Il database viene gestito localmente tramite `pg_ctl` e viene salvato in `./database/`.
 * Il modulo aggiorna lo stato globale (contenuto in `status.js`) e utilizza le costanti definite in `constants.js`.
 */

const { exec } = require("child_process");
const CONSTANTS = require("../constants");
const status = require("../status");
const { log, error } = require("console");

/**
 * Avvia il database PostgreSQL su una porta specificata.
 *
 * Se la porta predefinita è occupata, tenta di individuarne una alternativa randomica.
 * Se il database risulta già avviato, verifica che il database `homeharbor` esista.
 * Se non esiste, tenta un nuovo avvio su un'altra porta.
 *
 * @returns {Promise<number>} - Porta su cui è stato avviato correttamente il database
 */
function startDatabase() {
    return new Promise((resolve, reject) => {
        /**
         * Funzione ricorsiva che tenta di avviare il database su una porta specifica.
         * Se fallisce per conflitto o assenza del database, ritenta con una nuova porta casuale.
         */
        function attemptStart(port) {
            exec(
                `pg_ctl -D ./database -l ./database/postgresql.log start -o "-p ${port}"`,
                (err, stdout, stderr) => {
                    if (!err) {
                        log(
                            `✅ Database avviato correttamente sulla porta ${port}`
                        );
                        resolve(port);
                        return;
                    }

                    // 🔍 Se il database è già attivo o ha fallito l'avvio, procediamo con i controlli
                    if (
                        [
                            "un altro server",
                            "l'avvio del server è fallito",
                        ].some((e) => stderr.toString().includes(e))
                    ) {
                        log(
                            `❗️ Database già avviato sulla porta ${port},`,
                            `controllo la presenza del database ${status.databaseName}...`
                        );

                        // ✅ Verifica che il database sia effettivamente accessibile sulla porta corrente
                        exec(
                            `psql -p ${port} -c "SELECT 1" ${status.databaseName}`,
                            (err, stdout, stderr) => {
                                if (!err) {
                                    log(
                                        `✅ Database ${status.databaseName} trovato sulla porta ${port}`
                                    );
                                    resolve(port);
                                    return;
                                } else {
                                    // ❌ Database non trovato → tentiamo con una nuova porta casuale
                                    const newPort =
                                        Math.floor(Math.random() * 10000) +
                                        9999;
                                    log(`❌ Database ${status.databaseName} non trovato sulla porta ${port}, 
                                provo ad avviarlo sulla porta ${newPort}`);

                                    attemptStart(newPort); // 🔁 Riproviamo con una porta nuova
                                }
                            }
                        );
                    } else {
                        // ❌ Altri errori imprevisti nell'avvio del database
                        error(
                            `❌ Errore durante l'avvio del database: ${stderr}`
                        );
                        reject(stderr);
                    }
                }
            );
        }

        log("🚀 Avvio del database in corso...");
        attemptStart(CONSTANTS.DATABASE_PORT);
    });
}

/**
 * Arresta il database PostgreSQL in modo sicuro.
 *
 * Utilizza `pg_ctl stop` per fermare il processo in esecuzione nella directory `./database/`.
 *
 * @returns {Promise<void>}
 */
function quitDatabase() {
    return new Promise((resolve, reject) => {
        log("🛑 Arresto del database in corso...");
        exec(`pg_ctl -D ./database stop`, (err, stdout, stderr) => {
            if (!err) {
                log(`✅ Database arrestato correttamente`);
                resolve();
            } else {
                error(`❌ Errore durante l'arresto del database: ${stderr}`);
                reject(stderr);
            }
        });
    });
}

// ✅ Esportiamo le funzioni per l'utilizzo in openApp() e quitApp()
module.exports = {
    startDatabase,
    quitDatabase,
};
