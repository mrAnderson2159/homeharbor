// frontend/src/context/ThemeContext.js

/**
 * Context globale per la gestione del tema (light/dark) nell'applicazione HomeHarbor.
 *
 * Questo modulo fornisce:
 * - un provider (`ThemeProvider`) che carica e applica il tema all'avvio dell'app;
 * - una funzione `toggleTheme()` per passare da dark a light e viceversa;
 * - una custom hook `useTheme()` per accedere facilmente a tema e toggle ovunque.
 *
 * Le impostazioni vengono salvate e lette tramite l'API `window.settings`,
 * esposta nel preload di Electron. Questo garantisce persistenza tra i riavvii.
 *
 * Il tema viene applicato dinamicamente all'elemento `document.documentElement`
 * tramite l'attributo `data-theme`, rendendo facile la personalizzazione dei CSS.
 *
 * ⚠️ Questo context presuppone che il preload Electron esponga:
 *   - `window.settings.get(key)`
 *   - `window.settings.set(key, value)`
 */

import { createContext, useContext, useEffect, useState } from "react";

// Crea un contesto React per la gestione del tema
const ThemeContext = createContext();

/**
 * Componente provider da posizionare in alto nella gerarchia React,
 * tipicamente attorno ad `<App />`. Fornisce `theme` e `toggleTheme` ai figli.
 */
export const ThemeProvider = ({ children }) => {
    // Stato locale per il tema, inizialmente dark (fallback)
    const [theme, setTheme] = useState("dark");

    /**
     * Effetto eseguito una sola volta all'avvio.
     * Recupera il valore del tema persistito tramite Electron (`electron-store`),
     * se presente, e aggiorna lo stato locale.
     */
    useEffect(() => {
        window.settings.get("theme").then((saved) => {
            if (saved) setTheme(saved);
        });
    }, []);

    /**
     * Ogni volta che cambia `theme`, aggiorna l'attributo
     * `data-theme` nel root del documento.
     * Questo attributo può essere usato nel CSS per cambiare dinamicamente lo stile.
     */
    useEffect(() => {
        document.documentElement.setAttribute("data-theme", theme);
    }, [theme]);

    /**
     * Inverte il tema attuale (dark <-> light), aggiornando sia lo stato
     * locale sia la persistenza tramite l'API Electron.
     */
    const toggleTheme = () => {
        const newTheme = theme === "dark" ? "light" : "dark";
        setTheme(newTheme);
        window.settings.set("theme", newTheme);
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

/**
 * Custom hook per accedere rapidamente al contesto del tema
 * all'interno di un componente React.
 *
 * Esempio:
 *   const { theme, toggleTheme } = useTheme();
 */
export const useTheme = () => useContext(ThemeContext);
