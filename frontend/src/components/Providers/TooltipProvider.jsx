import { useEffect, useState } from "react";
import { Tooltip } from "bootstrap";

export default function TooltipProvider() {
    const [activeTooltips, setActiveTooltips] = useState([]);

    useEffect(() => {
        console.log("🧠 useEffect[init] -> mount");

        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );
        console.log(
            "🔍 Elementi con tooltip trovati:",
            tooltipTriggerList.length
        );

        tooltipTriggerList.forEach((el) => {
            console.log("✨ Tooltip inizializzato:", el);
            new Tooltip(el, {
                delay: { show: 1000, hide: 100 },
                placement: "right",
            });
        });

        const observer = new MutationObserver((mutationsList) => {
            for (const mutation of mutationsList) {
                mutation.addedNodes.forEach((node) => {
                    if (
                        node.nodeType === 1 &&
                        node.classList.contains("tooltip")
                    ) {
                        console.log("🟢 Tooltip aggiunto al DOM:", node);
                        setActiveTooltips((prev) => {
                            if (!prev.includes(node)) {
                                const updated = [...prev, node];
                                console.log(
                                    "📌 Stack aggiornato (add):",
                                    updated
                                );
                                return updated;
                            }
                            return prev;
                        });
                    }
                });

                mutation.removedNodes.forEach((node) => {
                    if (
                        node.nodeType === 1 &&
                        node.classList.contains("tooltip")
                    ) {
                        console.log("🔴 Tooltip rimosso dal DOM:", node);
                        setActiveTooltips((prev) => {
                            const updated = prev.filter((el) => el !== node);
                            console.log(
                                "📌 Stack aggiornato (remove):",
                                updated
                            );
                            return updated;
                        });
                    }
                });
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
        });

        return () => {
            console.log("🧹 useEffect[init] -> cleanup");

            observer.disconnect();

            tooltipTriggerList.forEach((el) => {
                const instance = Tooltip.getInstance(el);
                if (instance) {
                    console.log("🧨 Disposing tooltip:", el);
                    instance.dispose();
                }
            });
        };
    }, []);

    useEffect(() => {
        console.log("🎯 useEffect[activeTooltips] triggered:");
        console.log("📦 Stack attuale:", activeTooltips);

        const tooltipTriggerList = document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        );

        if (activeTooltips.length > 1) {
            const toRemove = activeTooltips[0];
            if (toRemove) {
                console.log("🧹 Rimuovo tooltip precedente:", toRemove);
                toRemove.remove();
            }

            setActiveTooltips((prev) => {
                const updated = prev.slice(1);
                console.log("📌 Stack aggiornato (slice):", updated);
                return updated;
            });

            tooltipTriggerList.forEach((el) => {
                console.log({ el, activeTooltips });

                console.log("⏱️ Reinit tooltip (delay 0):", el);
                new Tooltip(el, {
                    delay: { show: 0, hide: 100 },
                    placement: "right",
                });
            });
        } else if (activeTooltips.length === 1) {
            tooltipTriggerList.forEach((el) => {
                console.log("⏱️ Reinit tooltip (delay 1000):", el);
                new Tooltip(el, {
                    delay: { show: 1000, hide: 100 },
                    placement: "right",
                });
            });
        }
    }, [activeTooltips]);

    return null;
}
