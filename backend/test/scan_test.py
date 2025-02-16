import platform
import subprocess
import os
import time

# Determina il sistema operativo
system = platform.system()

# Importa solo le librerie necessarie in base all'OS
if system == "Windows":
    try:
        import pyinsane2
    except ImportError:
        print("⚠️ pyinsane2 non è installato. Usa `pip install pyinsane2`.")

def scan_document(output_filename="scanned_document.png"):
    """Scansiona un documento e lo salva come immagine."""
    if system == "Windows":
        return scan_windows(output_filename)
    elif system == "Linux":
        return scan_linux(output_filename)
    elif system == "Darwin":  # macOS
        return scan_mac(output_filename)
    else:
        print("❌ Sistema operativo non supportato!")
        return None

def scan_windows(output_filename):
    """Usa pyinsane2 per acquisire immagini su Windows con WIA/TWAIN."""
    if "pyinsane2" not in globals():
        print("❌ Errore: pyinsane2 non è disponibile su questo sistema.")
        return None

    try:
        pyinsane2.init()
        devices = pyinsane2.get_devices()

        if not devices:
            print("❌ Nessuno scanner trovato!")
            return None

        scanner = devices[0]  # Seleziona il primo scanner disponibile
        print(f"📸 Usando scanner: {scanner.name}")

        # Imposta la risoluzione a 300 DPI e modalità colore
        scanner.options["resolution"].value = 300
        scanner.options["mode"].value = "Color"

        scan_session = scanner.scan(multiple=False)
        while scan_session.running:
            scan_session.wait()

        image = scan_session.images[0]
        image.save(output_filename)
        print(f"✅ Immagine salvata come {output_filename}")
        return output_filename
    finally:
        pyinsane2.exit()

def scan_linux(output_filename):
    """Usa scanimage (SANE) per acquisire immagini su Linux."""
    if not is_command_available("scanimage"):
        print("❌ Errore: scanimage non è installato. Installa SANE (`sudo apt install sane-utils`).")
        return None

    try:
        subprocess.run(["scanimage", "--format=png", "-o", output_filename], check=True)
        print(f"✅ Immagine salvata come {output_filename}")
        return output_filename
    except subprocess.CalledProcessError:
        print("❌ Errore durante la scansione con scanimage!")
        return None

def scan_mac(output_filename):
    """Usa imagescan o AppleScript per acquisire immagini su macOS."""
    if is_command_available("imagescan"):
        try:
            subprocess.run([
                "imagescan",
                "--resolution", "300",
                "--mode", "Color",
                "--format", "png",
                "--output", output_filename
            ], check=True)
            print(f"✅ Immagine salvata come {output_filename}")
            return output_filename
        except subprocess.CalledProcessError:
            print("❌ Errore durante la scansione con imagescan!")
            return None
    else:
        print("⚠️ imagescan non trovato! Provo con AppleScript...")
        return scan_mac_applescript(output_filename)

def scan_mac_applescript(output_filename):
    """Usa AppleScript per acquisire immagini con Image Capture su macOS."""
    try:
        script_content = f"""
        tell application "Image Capture"
            set scannerList to every scanner
            if (count of scannerList) is 0 then
                error "❌ Nessuno scanner trovato!"
            else
                set scannerDevice to first item of scannerList
                set scanResults to scan scannerDevice into "{os.path.abspath(output_filename)}"
            end if
        end tell
        """

        # Scrive lo script in un file temporaneo
        script_path = "/tmp/scan_script.scpt"
        with open(script_path, "w") as script_file:
            script_file.write(script_content)

        # Esegue lo script
        subprocess.run(["osascript", script_path], check=True)
        print(f"✅ Immagine salvata come {output_filename}")
        return output_filename

    except subprocess.CalledProcessError:
        print("❌ Errore durante la scansione su macOS!")
        return None

def is_command_available(command):
    """Verifica se un comando è disponibile nel sistema."""
    return subprocess.run(["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0

if __name__ == "__main__":
    scan_document("documento_scansionato.png")