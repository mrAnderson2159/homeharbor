# 🛠️ HomeHarbor - Script di Setup Completo per Sviluppatori

Questo script `setup.sh` automatizza completamente l'installazione dell'ambiente di sviluppo per **HomeHarbor**, coprendo tutti i seguenti aspetti:

-   🔍 Rilevamento del sistema operativo
-   🐍 Installazione Python, virtualenv e dipendenze
-   ⚙️ Setup completo di NodeJS (Electron + Frontend)
-   🖨️ Configurazione opzionale dello scanner
-   🗃️ Configurazione del database PostgreSQL (initdb, pg_ctl, createuser, createdb)
-   🧬 Gestione Alembic (migrazioni automatiche)
-   🧪 Popolamento del database iniziale
-   🔗 Integrazione automatica degli alias sviluppatore (`aliases.zsh`)

---

## 📜 Uso

Per eseguire lo script:

```bash
chmod +x setup.sh
./setup.sh
```

---

## 🔧 Dettagli del funzionamento

1. **Individua il sistema operativo** (macOS, Linux, Windows).
2. Imposta `NULL_DEVICE` per gestire `stdout`/`stderr` in modo cross-platform.
3. Si sposta nella root del progetto (`SCRIPT_DIR`).
4. Installa Python e strumenti richiesti (`brew`, `apt`, `yum`, `choco`).
5. Crea e attiva un ambiente virtuale in `backend/venv`.
6. Esegue `npm install` in `electron/` e `frontend/`.
7. Installa le dipendenze Python con `pip install ./backend`.
8. Chiede se configurare lo scanner (solo macOS/Linux).
9. Verifica presenza cluster PostgreSQL in `database/`; se mancante, lo crea con `initdb`.
10. Avvia PostgreSQL sulla porta `15432` con `pg_ctl`.
11. Verifica e crea (se serve) il database `homeharbor` e il ruolo `postgres`.
12. Controlla se ci sono migrazioni in `alembic/versions`, altrimenti crea `init`.
13. Integra `aliases.zsh` in `~/.zshenv` se non già presente.
14. Esegue lo script `manage_database` per popolare il database.

---

## ✅ Requisiti

-   macOS, Linux o Windows con supporto Bash
-   Python ≥ 3.8
-   Node.js + npm
-   PostgreSQL
-   FastAPI + Uvicorn
-   Alembic
-   [cliclick](https://github.com/BlueM/cliclick) (macOS automation)

---

## 💡 Consigli

-   Per attivare subito gli alias, esegui:
    ```bash
    source ~/.zshenv
    ```
-   Se aggiungi nuovi alias a `aliases.zsh`, saranno automaticamente caricati alla prossima shell.
-   Puoi anche creare un alias per eseguire solo il popolamento DB:

```bash
alias homeharbor-populate='(cd backend && python -m app.paperless.manage_database)'
```
