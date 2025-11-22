const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export interface ChatResponse {
    response: string;
    citations?: { source: string; chunk: string }[];
}

export interface UploadResponse {
    filename: string;
    status: string;
    message: string;
}

export interface Settings {
    llm: string;
    vectorDb: string;
}

export const api = {
    async sendMessage(message: string, sessionId: string = 'default', settings?: Settings): Promise<ChatResponse> {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                session_id: sessionId,
                settings
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        return response.json();
    },

    async uploadFile(file: File, sessionId: string = 'default'): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', sessionId);

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to upload file');
        }

        return response.json();
    },

    async uploadFromGoogleDrive(fileId: string): Promise<UploadResponse> {
        const response = await fetch(`${API_BASE_URL}/upload/google-drive`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_id: fileId }),
        });

        if (!response.ok) {
            throw new Error('Failed to upload from Google Drive');
        }

        return response.json();
    },

    async getHealth(): Promise<{ status: string }> {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error('Backend is unhealthy');
        }
        return response.json();
    }
};
