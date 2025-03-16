// frontend/src/pages/Paperless/components/Form/Form.jsx

function commonFields(field, values) {
    return {
        id: field.id,
        label: field.label,
        onChange: field.onChange,
        value: values?.[field.id] ?? "",
        className: "form-control",
    };
}

function input(field, values) {
    return (
        <input
            type={field.type}
            name={field.name}
            placeholder={field.placeholder}
            min={field.min}
            max={field.max}
            {...commonFields(field, values)}
        />
    );
}

function select(field, values) {
    return (
        <select {...commonFields(field, values)}>
            {field.options.map((option) => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    );
}

export default function Form({
    fields = null,
    buttons = null,
    values = null,
    ...props
}) {
    return (
        <form {...props}>
            {fields &&
                fields.map((field) => (
                    <div key={field.id} className="mb-3">
                        <label htmlFor={field.id} className="form-label">
                            {field.label}
                        </label>
                        {field.type === "select" && select(field, values)}
                        {["number", "text"].includes(field.type) &&
                            input(field, values)}
                    </div>
                ))}
            <div className="d-flex justify-content-end">
                {buttons &&
                    buttons.map((button) => (
                        <button
                            key={button.text}
                            type={button.type}
                            className={`btn ${button.className}`}
                            onClick={button.onClick}
                        >
                            {button.text}
                        </button>
                    ))}
            </div>
        </form>
    );
}
