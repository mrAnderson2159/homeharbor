#!/bin/bash

# Nome dell'ambiente virtuale
VENV_DIR="backend/venv"

echo "⚙️  Inizio setup di HomeHarbor..."

# 1️⃣ Rilevare il sistema operativo
OS=$(uname)
case "$OS" in
    "Darwin")   OS="macOS" ;;
    "Linux")    OS="Linux" ;;
    "MINGW"*)   OS="Windows" ;;
    *)          echo "❌ Sistema operativo non supportato"; exit 1 ;;
esac
echo "🖥  Sistema rilevato: $OS"

# 🔇 Device nullo portabile
NULL_DEVICE="/dev/null"
[[ "$OS" == "Windows" ]] && NULL_DEVICE="NUL"

# 📁 Porta la working directory nella root del progetto (dove si trova questo script)
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> "$NULL_DEVICE" && pwd )"
cd "$SCRIPT_DIR" || {
  echo "❌ Impossibile accedere alla directory del progetto"; exit 1;
}
echo "📂 Directory di lavoro impostata su: $SCRIPT_DIR"


# 2️⃣ Installare Python e strumenti di base
if [[ "$OS" == "macOS" ]]; then
    if ! command -v brew &> /dev/null; then
        echo "🍺 Homebrew non trovato. Installazione in corso..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install python cliclick
elif [[ "$OS" == "Linux" ]]; then
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip hplip imagescan
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-venv python3-pip hplip imagescan
    fi
elif [[ "$OS" == "Windows" ]]; then
    if ! command -v choco &> /dev/null; then
        echo "🍫 Chocolatey non trovato. Installazione in corso..."
        powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        export PATH="$PATH:/c/ProgramData/chocolatey/bin"
    fi
    choco install python -y
fi

# 3️⃣ Creazione dell'ambiente virtuale
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creazione ambiente virtuale ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Ambiente virtuale già presente"
fi

# 4️⃣ Attivazione dell'ambiente virtuale
echo "🚀 Attivazione ambiente virtuale..."
if [[ "$OS" == "Windows" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# 5️⃣ Installazione dipendenze Node (electron)
echo "⬇️  Installazione dipendenze Node in electron/..."
( cd electron && npm install )

# 6️⃣ Aggiornamento pip e installazione del pacchetto backend
echo "⬇️  Aggiornamento pip + installazione backend..."
pip install --upgrade pip setuptools wheel
pip install ./backend

# 7️⃣ Installazione dipendenze frontend
echo "⬇️  Installazione dipendenze Node in frontend/..."
npm install
( cd frontend && npm install )

# 8️⃣ Setup scanner solo su macOS/Linux
if [[ "$OS" == "macOS" || "$OS" == "Linux" ]]; then
    echo ""
    read -p "🖨️  Vuoi configurare lo scanner ora? (y/N): " setup_scanner

    if [[ "$setup_scanner" =~ ^[Yy]$ ]]; then
        echo ""
        echo "🖨️ Quale scanner stai usando?"
        echo "1) HP"
        echo "2) Epson"
        echo "3) Altro / Nessuna installazione"
        read -p "Seleziona un'opzione (1/2/3): " scanner_choice

        case "$scanner_choice" in
            "1")
                echo "🔹 Installazione supporto HP..."
                [[ "$OS" == "macOS" ]] && brew install sane-backends
                ;;
            "2")
                echo "🔹 Installazione supporto Epson..."
                [[ "$OS" == "macOS" ]] && brew install imagescan
                ;;
            *) echo "⚠️ Nessun software per scanner installato" ;;
        esac
    else
        echo "🚫 Configurazione scanner saltata."
    fi
fi


echo "✅ Parte 1 completata: ambienti e scanner pronti"
