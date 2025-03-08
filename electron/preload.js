const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
    sendMessage: (message) => console.log("Messaggio ricevuto:", message),
});
