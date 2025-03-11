const { contextBridge, ipcRenderer } = require("electron");

// Espone API sicure in `window.settings`
contextBridge.exposeInMainWorld("settings", {
    get: (key) => ipcRenderer.invoke("settings:get", key),
    set: (key, value) => ipcRenderer.invoke("settings:set", key, value),
});
// 💡 Usiamo invoke perché ipcMain.handle e ipcRenderer.invoke sono asincroni
// e restituiscono Promise.
