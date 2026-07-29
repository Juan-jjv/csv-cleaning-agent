const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadCsv(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/upload`,
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail || "Failed to upload CSV."
        );
    }

    return response.json();
}

export async function cleanCsv(
    sessionId,
    instruction,
) {
    const response = await fetch(
        `${API_BASE_URL}/clean`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                session_id: sessionId,
                instruction: instruction,
            }),
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to clean CSV."
        );
    }

    return response.json();
}

export async function downloadCsv(sessionId) {
    const response = await fetch(
        `${API_BASE_URL}/download/${sessionId}`
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to download CSV."
        );
    }

    return response.blob();
}

export async function getDatasetPage(
    sessionId,
    page = 1,
    pageSize = 50,
) {
    const response = await fetch(
        `${API_BASE_URL}/data/${sessionId}?page=${page}&page_size=${pageSize}`
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to load dataset."
        );
    }

    return response.json();
}