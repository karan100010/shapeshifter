'use client';

import { useState, useEffect } from 'react';
import styles from './SettingsModal.module.css';

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (settings: Settings) => void;
    initialSettings: Settings;
}

export interface Settings {
    llm: string;
    vectorDb: string;
}

export const AVAILABLE_LLMS = [
    { id: 'gemma-27b', name: 'NVIDIA Gemma 27B' },
    { id: 'llama-3-70b', name: 'Meta Llama 3 70B' },
    { id: 'mistral-large', name: 'Mistral Large' },
    { id: 'gpt-4', name: 'GPT-4 (OpenAI)' }
];

export const AVAILABLE_VECTOR_DBS = [
    { id: 'qdrant', name: 'Qdrant' },
    { id: 'chroma', name: 'ChromaDB' },
    { id: 'milvus', name: 'Milvus' },
    { id: 'pgvector', name: 'PostgreSQL (pgvector)' }
];

export default function SettingsModal({ isOpen, onClose, onSave, initialSettings }: SettingsModalProps) {
    const [settings, setSettings] = useState<Settings>(initialSettings);

    useEffect(() => {
        setSettings(initialSettings);
    }, [initialSettings]);

    if (!isOpen) return null;

    const handleSave = () => {
        onSave(settings);
        onClose();
    };

    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <div className={styles.header}>
                    <h2>Settings</h2>
                    <button className={styles.closeBtn} onClick={onClose}>×</button>
                </div>

                <div className={styles.content}>
                    <div className={styles.section}>
                        <label className={styles.label}>LLM Model</label>
                        <select
                            className={styles.select}
                            value={settings.llm}
                            onChange={(e) => setSettings({ ...settings, llm: e.target.value })}
                        >
                            {AVAILABLE_LLMS.map(llm => (
                                <option key={llm.id} value={llm.id}>{llm.name}</option>
                            ))}
                        </select>
                        <p className={styles.description}>
                            Select the Large Language Model to use for generating responses.
                        </p>
                    </div>

                    <div className={styles.section}>
                        <label className={styles.label}>Vector Database</label>
                        <select
                            className={styles.select}
                            value={settings.vectorDb}
                            onChange={(e) => setSettings({ ...settings, vectorDb: e.target.value })}
                        >
                            {AVAILABLE_VECTOR_DBS.map(db => (
                                <option key={db.id} value={db.id}>{db.name}</option>
                            ))}
                        </select>
                        <p className={styles.description}>
                            Choose the vector database for storing and retrieving document embeddings.
                        </p>
                    </div>
                </div>

                <div className={styles.footer}>
                    <button className={styles.cancelBtn} onClick={onClose}>Cancel</button>
                    <button className={styles.saveBtn} onClick={handleSave}>Save Changes</button>
                </div>
            </div>
        </div>
    );
}
