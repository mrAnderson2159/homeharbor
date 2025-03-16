import "./ScannerWindow.scss";
import axios from "../../../../api/axios";
import { useEffect, useState } from "react";
import Form from "../Form/Form";

async function getFormStructure(setValues) {
    const response = await axios.get("/api/paperless/form/structure");
    const data = response.data;
    const defaultValues = {};

    data.forEach((field) => {
        // Se è un campo select e ha delle opzioni, seleziona la prima opzione
        if (
            field.type === "select" &&
            Array.isArray(field.options) &&
            field.options.length > 0
        ) {
            defaultValues[field.id] = field.options[0].value;
        }

        field.onChange = (event) => {
            bind(field.id, event.target.value, setValues);
        };
    });

    setValues(defaultValues);

    return data;
}

function bind(id, value, setValues) {
    setValues((prevValues) => ({
        ...prevValues,
        [id]: value,
    }));
}

export default function ScannerWindow() {
    const [formStructure, setFormStructure] = useState(null);
    const [values, setValues] = useState({});

    useEffect(() => {
        getFormStructure(setValues).then(setFormStructure);
    }, []);

    // useEffect(() => {
    //     console.log(values); // DEBUG
    // }, [values]);

    function handleSubmit(event) {
        event.preventDefault();
        console.log("📤 Submit:", values);
        // Qui puoi aggiungere la POST al backend!
    }

    function handleReset(event) {
        event.preventDefault();
        const reset = {};
        formStructure.forEach((field) => {
            reset[field.id] =
                field.type === "select" &&
                Array.isArray(field.options) &&
                field.options.length > 0
                    ? field.options[0].value
                    : "";
        });
        setValues(reset);
    }

    const buttons = [
        {
            text: "Reset",
            type: "button",
            className: "btn-secondary me-2",
            onClick: handleReset,
        },
        {
            text: "Invia",
            type: "submit",
            className: "btn-primary",
            onClick: handleSubmit,
        },
    ];

    return (
        <div>
            <Form fields={formStructure} values={values} buttons={buttons} />
        </div>
    );
}
