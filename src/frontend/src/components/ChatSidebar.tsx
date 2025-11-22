'use client';

import styles from './ChatSidebar.module.css';

interface Chat {
    id: string;
    title: string;
    timestamp: Date;
}

interface ChatSidebarProps {
    chats: Chat[];
    activeChat: string;
    onChatSelect: (chatId: string) => void;
    onNewChat: () => void;
    onSettingsClick?: () => void;
}

export default function ChatSidebar({ chats, activeChat, onChatSelect, onNewChat, onSettingsClick }: ChatSidebarProps) {
    return (
        <aside className={styles.sidebar}>
            <div className={styles.header}>
                <h2 className={styles.title}>ShapeShifter</h2>
                <p className={styles.subtitle}>RAG Assistant</p>
            </div>

            <button className={styles.newChatBtn} onClick={onNewChat}>
                <span className={styles.icon}>➕</span>
                New Chat
            </button>

            <div className={styles.chatList}>
                <h3 className={styles.sectionTitle}>Recent Chats</h3>
                {chats.map(chat => (
                    <button
                        key={chat.id}
                        className={`${styles.chatItem} ${activeChat === chat.id ? styles.active : ''}`}
                        onClick={() => onChatSelect(chat.id)}
                    >
                        <span className={styles.chatIcon}>💬</span>
                        <div className={styles.chatInfo}>
                            <div className={styles.chatTitle}>{chat.title}</div>
                            <div className={styles.chatTime}>
                                {chat.timestamp.toLocaleDateString()}
                            </div>
                        </div>
                    </button>
                ))}
            </div>

            <div className={styles.footer}>
                <button className={styles.footerBtn} onClick={onSettingsClick}>
                    <span>⚙️</span> Settings
                </button>
                <button className={styles.footerBtn}>
                    <span>📚</span> Documents
                </button>
            </div>
        </aside>
    );
}
