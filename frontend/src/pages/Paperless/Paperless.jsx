// frontend/src/pages/Paperless/Paperless.jsx
import "./Paperless.scss";
import { useState } from "react";
import PageContainer from "../../components/Layout/PageContainer";
import ControlDeck from "../../components/Layout/ControlDeck/ControlDeck";
import ScannerWindow from "./components/ScannerWindow/ScannerWindow";
import ManageWindow from "./components/ManageWindow/ManageWindow";
import SearchWindow from "./components/SearchWindow/SearchWindow";
import UploadWindow from "./components/UploadWindow/UploadWindow";

const components = {
    scanner: ScannerWindow,
    manager: ManageWindow,
    search: SearchWindow,
    upload: UploadWindow,
};

function tooltipText(tab) {
    const map = {
        scanner: "Scannerizza documenti",
        manager: "Gestione documenti",
        search: "Cerca tra i documenti",
        upload: "Carica nuovi documenti",
    };
    return map[tab] ?? "";
}

export default function Paperless() {
    const [activeTab, setActiveTab] = useState("scanner");

    const controlDeckData = [
        { icon: "bi bi-file-break", tab: "scanner" }, // stessa icona di Paperless in Home
        { icon: "bi bi-pencil-square", tab: "manager" }, // per editing/gestione
        { icon: "bi bi-search", tab: "search" }, // lente classica
        { icon: "bi bi-upload", tab: "upload" }, // freccia verso l'alto
    ];

    const ActiveWindow = components[activeTab];

    return (
        <PageContainer className="d-flex flex-row paperless">
            <ControlDeck
                data={controlDeckData}
                clickHandler={setActiveTab}
                activeTab={activeTab}
                tooltipText={tooltipText}
            />
            <div className="paperless__window">
                <ActiveWindow />
            </div>
        </PageContainer>
    );
}
