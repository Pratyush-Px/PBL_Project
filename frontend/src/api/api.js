const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const compareDocuments = async (orderFile, invoiceFile) => {
    const formData = new FormData();
    formData.append("purchase_order", orderFile);
    formData.append("invoice", invoiceFile);

    try {
        const response = await fetch(`${API_URL}/compare`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || "Comparison failed");
        }

        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
