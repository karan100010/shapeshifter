'use client';

import { useState, type KeyboardEvent } from 'react';
import styles from './ChatInput.module.css';

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
    const [message, setMessage] = useState('');

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
                <button className={styles.uploadBtn} title="Upload document">
                    📎
                </button>
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
