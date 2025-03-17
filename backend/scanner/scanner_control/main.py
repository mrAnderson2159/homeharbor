# backend/scanner/scanner_control/main.py
from scanner_control.automation import click_scan_button

def main():
    print("🖨️ Avviando il processo di scansione...")
    click_scan_button()

if __name__ == "__main__":
    main()