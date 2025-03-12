// frontend/src/pages/Home/Home.jsx
import PageContainer from "../../components/Layout/PageContainer";
import SectionCard from "./components/SectionCard/SectionCard";
import "./Home.scss";

class PageDetails {
    constructor(title, page, icon, description) {
        this.title = title;
        this.page = page;
        this.icon = icon;
        this.description = description;
    }
}

export default function Home() {
    const pages = [
        {
            title: "Paperless",
            page: "/paperless",
            icon: "bi bi-file-break",
            description:
                "Scannerizza, Archivia, Cerca e Gestisci i tuoi documenti",
        },
        {
            title: "Firma Digitale",
            page: "/firma",
            icon: "bi bi-pencil-square",
            description: "Firma i tuoi documenti digitalmente",
        },
        {
            title: "Archiviazione",
            page: "/archiviazione",
            icon: "bi bi-archive",
            description: "Archivia i tuoi documenti in modo sicuro",
        },
        {
            title: "Condivisione",
            page: "/condivisione",
            icon: "bi bi-share",
            description: "Condividi i tuoi documenti con chi vuoi",
        },
    ];

    return (
        <PageContainer>
            <div className="row h-100">
                {pages.map((page, index) => (
                    <div className="col-6 p-0 h-50" key={index}>
                        <SectionCard
                            title={page.title}
                            page={page.page}
                            icon={page.icon}
                            description={page.description}
                        />
                    </div>
                ))}
            </div>
        </PageContainer>
    );
}
