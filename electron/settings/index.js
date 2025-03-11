const Store = require("electron-store").default;
const defaults = require("./defaults");

const store = new Store({ defaults });

module.exports = {
    get: (key) => store.get(key),
    set: (key, value) => store.set(key, value),
    getAll: () => store.store,
};
