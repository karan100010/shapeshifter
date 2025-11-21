'use client';

import { useState } from 'react';
import styles from './Message.module.css';

interface Citation {
    source: string;
    chunk: string;
}

interface MessageProps {
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    citations?: Citation[];
}

export default function Message({ role, content, timestamp, citations }: MessageProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`${styles.message} ${styles[role]}`}>
            <div className={styles.avatar}>
                {role === 'user' ? '👤' : '🤖'}
            </div>
            <div className={styles.content}>
                <div className={styles.bubble}>
                    <p className={styles.text}>{content}</p>
                    {citations && citations.length > 0 && (
                        <div className={styles.citations}>
                            <div className={styles.citationsHeader}>📚 Sources:</div>
                            {citations.map((citation, idx) => (
                                <div key={idx} className={styles.citation}>
                                    <span className={styles.citationNumber}>[{idx + 1}]</span>
                                    <span className={styles.citationSource}>{citation.source}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
                <div className={styles.meta}>
                    <span className={styles.timestamp}>
                        {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    {role === 'assistant' && (
                        <button
                            className={styles.copyBtn}
                            onClick={handleCopy}
                            title="Copy message"
                        >
                            {copied ? '✓ Copied' : '📋 Copy'}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
