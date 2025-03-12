// frontend/src/components/Elements/Icon.jsx
export default function Icon({
    icon,
    type = "i",
    includeDiv = true,
    ...props
}) {
    let iconElement = null;

    switch (type) {
        case "img":
            iconElement = <img src={icon} alt="icon" />;
            break;
        case "i":
        default:
            iconElement = <i className={icon}></i>;
    }

    return includeDiv ? (
        <div className="icon" {...props}>
            {iconElement}
        </div>
    ) : (
        iconElement
    );
}
