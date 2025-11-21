'use client';

import { useState, useRef, type KeyboardEvent, type ChangeEvent } from 'react';
import styles from './ChatInput.module.css';

interface ChatInputProps {
    onSend: (message: string) => void;
    onFileUpload?: (files: FileList) => void;
    disabled?: boolean;
}

export default function ChatInput({ onSend, onFileUpload, disabled = false }: ChatInputProps) {
    const [message, setMessage] = useState('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleSend = () => {
        if (message.trim() && !disabled) {
            onSend(message.trim());
            setMessage('');
        }
    };

    const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleFileClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0 && onFileUpload) {
            onFileUpload(e.target.files);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.suggestions}>
                <button
                    className={styles.suggestion}
                    onClick={() => setMessage('What documents are available?')}
                >
                    💡 What documents are available?
                </button>
                <button
                    className={styles.suggestion}
                    onClick={() => setMessage('Explain the main concepts')}
                >
                    💡 Explain the main concepts
                </button>
                <button
                    className={styles.suggestion}
                    onClick={() => setMessage('Summarize the key findings')}
                >
                    💡 Summarize the key findings
                </button>
            </div>
            <div className={styles.inputArea}>
                <button
                    className={styles.uploadBtn}
                    title="Upload document"
                    onClick={handleFileClick}
                    type="button"
                >
                    📎
                </button>
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept=".pdf,.txt,.docx,.doc"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />
                <textarea
                    className={styles.input}
                    placeholder="Ask me anything about your documents..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={disabled}
                    rows={1}
                />
                <button
                    className={styles.sendBtn}
                    onClick={handleSend}
                    disabled={disabled || !message.trim()}
                    aria-label="Send message"
                >
                    <span className={styles.sendIcon}>➤</span>
                </button>
            </div>
        </div>
    );
}
