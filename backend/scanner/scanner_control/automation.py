# backend/scanner/scanner_control/automation.py
import time
import pyautogui
from backend.scanner_control.applescript import bring_hp_smart_to_front, get_window_geometry

def click_scan_button():
    """Porta HP Smart in primo piano e clicca il pulsante di scansione."""
    print("⌛ Portando HP Smart in primo piano...")
    bring_hp_smart_to_front()
    # time.sleep(2)  # Attendi caricamento UI

    geometry = get_window_geometry()
    if geometry:
        x, y, w, h = geometry
        click_x = x + w - 100  # Spostiamo il punto un po' a sinistra dell'angolo destro
        click_y = y + h - 50   # Spostiamo il punto un po' più in alto dell'angolo inferiore

        print(f"🖱️ Cliccando su ({click_x}, {click_y})")
        pyautogui.click(click_x, click_y)
    else:
        print("❌ Errore nel recuperare la posizione della finestra.")