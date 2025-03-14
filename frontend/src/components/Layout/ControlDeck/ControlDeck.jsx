// frontend/src/components/Layout/ControlDeck/ControlDeck.jsx
import "./ControlDeck.scss";
import Icon from "../../Elements/Icon";

export default function ControlDeck({
    data,
    iconType,
    clickHandler,
    activeTab,
    tooltipText,
    ...props
}) {
    // TYPE: data = [{icon, tab}, ...]
    return (
        <div className="control-deck" {...props}>
            <div className="control-deck__button-container">
                {data.map((item, index) => {
                    const { icon, tab } = item;
                    return (
                        <button
                            key={index}
                            className={`control-deck__button ${
                                tab === activeTab ? "active" : ""
                            }`}
                            onClick={() => clickHandler(tab)}
                            data-bs-toggle="tooltip"
                            data-bs-placement="right"
                            title={tooltipText(tab)}
                        >
                            <Icon icon={icon} type={iconType} />
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
