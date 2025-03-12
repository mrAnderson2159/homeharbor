// frontend/src/components/SectionCard/SectionCard.jsx
import "./SectionCard.scss";
import { Link } from "react-router-dom";
import Icon from "../../../../components/Elements/Icon";

export default function SectionCard({
    title,
    page,
    icon,
    description,
    IconType,
}) {
    return (
        <Link to={page} className="section-card">
            <Icon icon={icon} type={IconType} className="section-card__icon" />
            <div className="section-card__header">
                <h2 className="section-card__title">{title}</h2>
            </div>
            <p className="section-card__description">{description}</p>
        </Link>
    );
}
