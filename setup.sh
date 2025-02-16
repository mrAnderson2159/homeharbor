#!/bin/bash

# Nome dell'ambiente virtuale
VENV_DIR="venv"

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

# 2️⃣ Installare Python e il gestore pacchetti corretto
if [[ "$OS" == "macOS" ]]; then
    if ! command -v brew &> /dev/null; then
        echo "🍺 Homebrew non trovato. Installazione in corso..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install python
elif [[ "$OS" == "Linux" ]]; then
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-venv python3-pip
    fi
elif [[ "$OS" == "Windows" ]]; then
    if ! command -v choco &> /dev/null; then
        echo "🍫 Chocolatey non trovato. Installazione in corso..."
        powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        export PATH="$PATH:/c/ProgramData/chocolatey/bin"
    fi
    choco install python -y
fi

# 3️⃣ Creare l'ambiente virtuale se non esiste
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creazione ambiente virtuale ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Ambiente virtuale creato!"
else
    echo "✅ Ambiente virtuale già presente!"
fi

# 4️⃣ Attivare il venv
echo "🚀 Attivazione ambiente virtuale..."
if [[ "$OS" == "Windows" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# 5️⃣ Assicurarsi che pip, setuptools e wheel siano installati
echo "⬇️  Aggiornamento pip, setuptools e wheel..."
pip install --upgrade pip setuptools wheel

# 6️⃣ Chiedere quale scanner si sta utilizzando su macOS/Linux
if [[ "$OS" == "macOS" || "$OS" == "Linux" ]]; then
    echo ""
    echo "🖨️ Quale scanner stai usando?"
    echo "1) HP"
    echo "2) Epson"
    echo "3) Altro / Non installare nulla"
    read -p "Seleziona un'opzione (1/2/3): " scanner_choice

    if [[ "$scanner_choice" == "1" ]]; then
        if [[ "$OS" == "macOS" ]]; then
            echo "🔹 Installazione di sane-backends per scanner HP su macOS..."
            brew install sane-backends
            echo "🔹 Per scanner HP, usa HP Smart: https://apps.apple.com/app/hp-smart-for-desktop/id1474276998"
        elif [[ "$OS" == "Linux" ]]; then
            echo "🔹 Installazione di HPLIP per scanner HP su Linux..."
            sudo apt install -y hplip || sudo yum install -y hplip
        fi
    elif [[ "$scanner_choice" == "2" ]]; then
        echo "🔹 Installazione di ImageScan per scanner Epson..."
        if [[ "$OS" == "macOS" ]]; then
            brew install imagescan#!/bin/bash

# Nome dell'ambiente virtuale
VENV_DIR="venv"

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

# 2️⃣ Installare Python e il gestore pacchetti corretto
if [[ "$OS" == "macOS" ]]; then
    if ! command -v brew &> /dev/null; then
        echo "🍺 Homebrew non trovato. Installazione in corso..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install python
elif [[ "$OS" == "Linux" ]]; then
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-venv python3-pip
    fi
elif [[ "$OS" == "Windows" ]]; then
    if ! command -v choco &> /dev/null; then
        echo "🍫 Chocolatey non trovato. Installazione in corso..."
        powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        export PATH="$PATH:/c/ProgramData/chocolatey/bin"
    fi
    choco install python -y
fi

# 3️⃣ Creare l'ambiente virtuale se non esiste
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creazione ambiente virtuale ($VENV_DIR)..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Ambiente virtuale creato!"
else
    echo "✅ Ambiente virtuale già presente!"
fi

# 4️⃣ Attivare il venv
echo "🚀 Attivazione ambiente virtuale..."
if [[ "$OS" == "Windows" ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

# 5️⃣ Assicurarsi che pip, setuptools e wheel siano installati
echo "⬇️  Aggiornamento pip, setuptools e wheel..."
pip install --upgrade pip setuptools wheel

# 6️⃣ Chiedere quale scanner si sta utilizzando su macOS/Linux
if [[ "$OS" == "macOS" || "$OS" == "Linux" ]]; then
    echo ""
    echo "🖨️ Quale scanner stai usando?"
    echo "1) HP"
    echo "2) Epson"
    echo "3) Altro / Non installare nulla"
    read -p "Seleziona un'opzione (1/2/3): " scanner_choice

    if [[ "$scanner_choice" == "1" ]]; then
        if [[ "$OS" == "macOS" ]]; then
            echo "🔹 Installazione di sane-backends per scanner HP su macOS..."
            brew install sane-backends
            echo "🔹 Per scanner HP, usa HP Smart: https://apps.apple.com/app/hp-smart-for-desktop/id1474276998"
        elif [[ "$OS" == "Linux" ]]; then
            echo "🔹 Installazione di HPLIP per scanner HP su Linux..."
            sudo apt install -y hplip || sudo yum install -y hplip
        fi
    elif [[ "$scanner_choice" == "2" ]]; then
        echo "🔹 Installazione di ImageScan per scanner Epson..."
        if [[ "$OS" == "macOS" ]]; then
            brew install imagescan
        elif [[ "$OS" == "Linux" ]]; then
            sudo apt install -y imagescan
        fi
    else
        echo "⚠️ Nessun software per scanner installato. Assicurati di avere i driver giusti."
    fi
fi
# 7️⃣ Installare le dipendenze con setup.py
echo "⬇️  Installazione dipendenze con setup.py..."
( cd backend && pip install . && cd .. )

# 8️⃣ Installare strumenti aggiuntivi
echo "⬇️  Installazione di strumenti di automazione..."
brew install cliclick  # Installiamo cliclick per automazione mouse

echo "✅ Dipendenze installate con successo!"

# 9️⃣ Aggiungere attivazione automatica al terminale
if [[ "$OS" == "macOS" || "$OS" == "Linux" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
    [[ -f "$HOME/.bashrc" ]] && PROFILE_FILE="$HOME/.bashrc"
    [[ -f "$HOME/.bash_profile" ]] && PROFILE_FILE="$HOME/.bash_profile"

    if ! grep -q "source $(pwd)/$VENV_DIR/bin/activate" "$PROFILE_FILE"; then
        echo "🔧 Aggiungo l'attivazione automatica del venv a $PROFILE_FILE..."
        echo "source $(pwd)/$VENV_DIR/bin/activate" >> "$PROFILE_FILE"
        echo "✅ Fatto! Riavvia il terminale o esegui 'source $PROFILE_FILE' per attivare il venv automaticamente."
    else
        echo "✅ Il venv è già impostato per l'attivazione automatica."
    fi
elif [[ "$OS" == "Windows" ]]; then
    echo "⚠️  Su Windows, attiva il venv con: venv\Scripts\activate"
fi

echo "🎉 Setup completato! Ora puoi eseguire il progetto."
        elif [[ "$OS" == "Linux" ]]; then
            sudo apt install -y imagescan
        fi
    else
        echo "⚠️ Nessun software per scanner installato. Assicurati di avere i driver giusti."
    fi
fi
# 7️⃣ Installare le dipendenze con setup.py
echo "⬇️  Installazione dipendenze con setup.py..."
( cd backend && pip install . && cd .. )

# 8️⃣ Installare strumenti aggiuntivi
echo "⬇️  Installazione di strumenti di automazione..."
brew install cliclick  # Installiamo cliclick per automazione mouse

echo "✅ Dipendenze installate con successo!"

# 9️⃣ Aggiungere attivazione automatica al terminale
if [[ "$OS" == "macOS" || "$OS" == "Linux" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
    [[ -f "$HOME/.bashrc" ]] && PROFILE_FILE="$HOME/.bashrc"
    [[ -f "$HOME/.bash_profile" ]] && PROFILE_FILE="$HOME/.bash_profile"

    if ! grep -q "source $(pwd)/$VENV_DIR/bin/activate" "$PROFILE_FILE"; then
        echo "🔧 Aggiungo l'attivazione automatica del venv a $PROFILE_FILE..."
        echo "source $(pwd)/$VENV_DIR/bin/activate" >> "$PROFILE_FILE"
        echo "✅ Fatto! Riavvia il terminale o esegui 'source $PROFILE_FILE' per attivare il venv automaticamente."
    else
        echo "✅ Il venv è già impostato per l'attivazione automatica."
    fi
elif [[ "$OS" == "Windows" ]]; then
    echo "⚠️  Su Windows, attiva il venv con: venv\Scripts\activate"
fi

echo "🎉 Setup completato! Ora puoi eseguire il progetto."