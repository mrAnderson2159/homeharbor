# backend/scanner/scanner_control/vision.py
import cv2
import numpy as np

def find_button_on_screen(image_path, template_path):
    """Usa OpenCV per trovare il pulsante 'Scansione' nello screenshot."""
    print("🔍 Cercando il pulsante 'Scansione'...")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if image is None or template is None:
        print("❌ Errore nel caricamento delle immagini!")
        return None, None

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.7:
        return max_loc
    else:
        print("❌ Pulsante non trovato!")
        return None, None