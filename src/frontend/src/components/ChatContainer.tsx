'use client';

import { useRef, useEffect } from 'react';
import Message from './Message';
import ChatInput from './ChatInput';
import styles from './ChatContainer.module.css';

interface MessageType {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    citations?: { source: string; chunk: string }[];
}

interface ChatContainerProps {
    messages: MessageType[];
    onSendMessage: (content: string) => void;
    onFileUpload?: (files: FileList) => void;
}

export default function ChatContainer({ messages, onSendMessage, onFileUpload }: ChatContainerProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Check if AI is currently typing (last message is from user)
    const isTyping = messages.length > 0 && messages[messages.length - 1].role === 'user';

    return (
        <div className={styles.container}>
            <div className={styles.messagesArea}>
                <div className={styles.messages}>
                    {messages.map(msg => (
                        <Message
                            key={msg.id}
                            role={msg.role}
                            content={msg.content}
                            timestamp={msg.timestamp}
                            citations={msg.citations}
                        />
                    ))}
                    {isTyping && (
                        <div className={styles.typingIndicator}>
                            <div className={styles.avatar}>🤖</div>
                            <div className={styles.typingBubble}>
                                <span className={styles.dot}></span>
                                <span className={styles.dot}></span>
                                <span className={styles.dot}></span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>
            <ChatInput onSend={onSendMessage} onFileUpload={onFileUpload} disabled={isTyping} />
        </div>
    );
}
