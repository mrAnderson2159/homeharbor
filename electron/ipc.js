const { ipcMain } = require("electron");
const settings = require("./settings");

// ESEMPIO: React dice: "dammi 'theme'"
ipcMain.handle("settings:get", (event, key) => {
    return settings.get(key);
});

// ESEMPIO: React dice: "imposta 'theme' su 'dark'"
ipcMain.handle("settings:set", (event, key, value) => {
    settings.set(key, value);
});
