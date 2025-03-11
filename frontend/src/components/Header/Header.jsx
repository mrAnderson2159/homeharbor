import "./Header.scss";
import logo from "../../assets/logo.png";

export default function Header() {
    return (
        <nav className="navbar px-3 py-2 hh-navbar" data-bs-theme="dark">
            <div className="container-fluid d-flex justify-content-between align-items-center">
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#sidebar"
                    aria-controls="sidebar"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon" />
                </button>

                <div className="d-flex align-items-center gap-4">
                    <img src={logo} alt="HomeHarbor logo" className="hh-logo" />
                    <span className="hh-title">HomeHarbor</span>
                </div>

                {/* Placeholder per elementi futuri a destra */}
                <div className="d-none d-lg-block" />
            </div>
        </nav>
    );
}
