const API_URL = "https://pbl-projectbackend.onrender.com"; // Adjust if needed

export const compareDocuments = async (orderFile, invoiceFile) => {
    const formData = new FormData();
    formData.append("order_file", orderFile);
    formData.append("invoice_file", invoiceFile);

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
