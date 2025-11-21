'use client';

import { useState } from 'react';
import ChatSidebar from '@/components/ChatSidebar';
import ChatContainer from '@/components/ChatContainer';
import styles from './page.module.css';

interface MessageType {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: { source: string; chunk: string }[];
}

interface Chat {
  id: string;
  title: string;
  timestamp: Date;
  messages: MessageType[];
}

export default function Home() {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: '1',
      title: 'Document Analysis',
      timestamp: new Date(Date.now() - 3600000),
      messages: [
        {
          id: '1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date(Date.now() - 3600000),
        }
      ]
    },
    {
      id: '2',
      title: 'Query about entities',
      timestamp: new Date(Date.now() - 7200000),
      messages: [
        {
          id: '2-1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date(Date.now() - 7200000),
        }
      ]
    },
    {
      id: '3',
      title: 'Graph relationships',
      timestamp: new Date(Date.now() - 86400000),
      messages: [
        {
          id: '3-1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date(Date.now() - 86400000),
        }
      ]
    },
  ]);
  const [activeChat, setActiveChat] = useState('1');

  const handleChatSelect = (chatId: string) => {
    setActiveChat(chatId);
  };

  const handleNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'New Chat',
      timestamp: new Date(),
      messages: [
        {
          id: `${Date.now()}-welcome`,
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date(),
        }
      ]
    };
    setChats(prev => [newChat, ...prev]);
    setActiveChat(newChat.id);
  };

  const handleSendMessage = (content: string) => {
    const currentChat = chats.find(c => c.id === activeChat);
    if (!currentChat) return;

    // Add user message
    const userMessage: MessageType = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    // Update chat with user message
    setChats(prev => prev.map(chat =>
      chat.id === activeChat
        ? { ...chat, messages: [...chat.messages, userMessage], timestamp: new Date() }
        : chat
    ));

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I received your query: "${content}". In a production environment, this would connect to the RAG backend to retrieve relevant documents and generate a response using the hybrid retrieval system (vector + sparse + graph).`,
        timestamp: new Date(),
        citations: [
          { source: 'document_1.pdf', chunk: 'Page 5, Section 2.1' },
          { source: 'document_2.pdf', chunk: 'Page 12, Section 4.3' },
        ]
      };

      setChats(prev => prev.map(chat =>
        chat.id === activeChat
          ? { ...chat, messages: [...chat.messages, aiMessage] }
          : chat
      ));

      // Update chat title based on first user message
      if (currentChat.title === 'New Chat' && currentChat.messages.length === 1) {
        const newTitle = content.slice(0, 30) + (content.length > 30 ? '...' : '');
        setChats(prev => prev.map(chat =>
          chat.id === activeChat
            ? { ...chat, title: newTitle }
            : chat
        ));
      }
    }, 1500);
  };

  const currentChat = chats.find(c => c.id === activeChat);

  return (
    <div className={styles.container}>
      <ChatSidebar
        chats={chats}
        activeChat={activeChat}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
      />
      <main className={styles.main}>
        {currentChat && (
          <ChatContainer
            chatId={currentChat.id}
            messages={currentChat.messages}
            onSendMessage={handleSendMessage}
          />
        )}
      </main>
    </div>
  );
}
