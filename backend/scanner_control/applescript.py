import subprocess
import re

def bring_hp_smart_to_front():
    """Porta HP Smart in primo piano."""
    script = '''
    tell application "System Events"
        tell process "HP Smart"
            set frontmost to true
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)

def get_window_geometry():
    """Recupera la posizione e dimensione della finestra di HP Smart e pulisce i dati."""
    script = '''
    tell application "System Events"
        tell process "HP Smart"
            set win to window "Scansione"
            set {x, y} to position of win
            set {w, h} to size of win
            return x & "," & y & "," & w & "," & h
        end tell
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    raw_output = result.stdout.strip()

    # print(f"📜 Output grezzo di AppleScript: {raw_output}")  # Debug

    # 🛠 Puliamo gli spazi extra e le virgole ripetute
    cleaned_output = re.sub(r'\s*,\s*', ',', raw_output).strip()  # Rimpiazza " , " con ","
    coords = cleaned_output.split(",")
    coords = list(filter(bool, coords))  # Rimuove stringhe vuote

    if len(coords) == 4:
        try:
            return tuple(map(int, coords))
        except ValueError:
            print(f"❌ Errore nella conversione delle coordinate: {coords}")
            return None
    else:
        print(f"❌ AppleScript ha restituito un formato errato: {coords}")
        return None