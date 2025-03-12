// frontend/src/components/Header/Header.jsx
import "./Header.scss";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";

export default function Header() {
    return (
        <nav className="navbar px-3 py-2 hh-navbar hh-header">
            <div className="container-fluid d-flex justify-content-between">
                <Link to="/" className="navbar-brand">
                    <div className="d-flex align-items-center gap-3">
                        <img
                            src={logo}
                            alt="HomeHarbor logo"
                            className="hh-logo"
                        />
                        <span className="hh-title">HomeHarbor</span>
                    </div>
                </Link>
                {/* Placeholder per elementi futuri a destra */}
                <div className="d-none d-lg-block" />
            </div>
        </nav>
    );
}
