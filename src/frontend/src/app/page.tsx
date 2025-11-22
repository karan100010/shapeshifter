'use client';

import { useState } from 'react';
import ChatSidebar from '@/components/ChatSidebar';
import ChatContainer from '@/components/ChatContainer';
import ThemeToggle from '@/components/ThemeToggle';
import styles from './page.module.css';
import SettingsModal, { Settings } from '@/components/SettingsModal';
import { api } from '@/lib/api';

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
      timestamp: new Date('2024-01-01T10:00:00'),
      messages: [
        {
          id: '1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date('2024-01-01T10:00:00'),
        }
      ]
    },
    {
      id: '2',
      title: 'Query about entities',
      timestamp: new Date('2024-01-01T09:00:00'),
      messages: [
        {
          id: '2-1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date('2024-01-01T09:00:00'),
        }
      ]
    },
    {
      id: '3',
      title: 'Graph relationships',
      timestamp: new Date('2024-01-01T08:00:00'),
      messages: [
        {
          id: '3-1',
          role: 'assistant',
          content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
          timestamp: new Date('2024-01-01T08:00:00'),
        }
      ]
    },
  ]);
  const [activeChat, setActiveChat] = useState('1');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [settings, setSettings] = useState<Settings>({
    llm: 'gemma-27b',
    vectorDb: 'qdrant'
  });

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

  const handleSendMessage = async (content: string) => {
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

    try {
      // Call backend API with settings
      const data = await api.sendMessage(content, activeChat, settings);

      const aiMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        citations: data.citations
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
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to chat
      const errorMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error connecting to the server. Please try again later.',
        timestamp: new Date(),
      };
      setChats(prev => prev.map(chat =>
        chat.id === activeChat
          ? { ...chat, messages: [...chat.messages, errorMessage] }
          : chat
      ));
    }
  };

  const handleFileUpload = async (files: FileList) => {
    console.log('Files uploaded in chat:', Array.from(files).map(f => f.name));
    console.log('Current session ID (activeChat):', activeChat);

    const fileArray = Array.from(files);
    const uploadedFiles = [];
    const failedFiles = [];

    for (const file of fileArray) {
      try {
        console.log(`Uploading ${file.name} to session ${activeChat}...`);
        const result = await api.uploadFile(file, activeChat);
        uploadedFiles.push(file.name);
        console.log(`✅ Uploaded: ${file.name}`, result);
      } catch (error) {
        console.error(`❌ Failed to upload ${file.name}:`, error);
        failedFiles.push(file.name);
      }
    }

    console.log('Upload complete. Uploaded:', uploadedFiles, 'Failed:', failedFiles);

    // Add a system message showing what was uploaded
    if (uploadedFiles.length > 0 || failedFiles.length > 0) {
      const systemMessage: MessageType = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `📎 **File Upload Status:**\n\n${uploadedFiles.length > 0
          ? `✅ Successfully uploaded:\n${uploadedFiles.map(f => `- ${f}`).join('\n')}\n\n`
          : ''
          }${failedFiles.length > 0
            ? `❌ Failed to upload:\n${failedFiles.map(f => `- ${f}`).join('\n')}\n\n`
            : ''
          }${uploadedFiles.length > 0 ? 'Proceeding to next step...' : ''}`,
        timestamp: new Date(),
      };

      setChats(prev => prev.map(chat =>
        chat.id === activeChat
          ? { ...chat, messages: [...chat.messages, systemMessage] }
          : chat
      ));

      // Automatically progress to next step if files were uploaded successfully
      if (uploadedFiles.length > 0) {
        console.log('Auto-sending "uploaded" message in 500ms...');
        // Wait a moment for the UI to update, then send "uploaded" automatically
        setTimeout(() => {
          console.log('Sending "uploaded" message now');
          handleSendMessage('uploaded');
        }, 500);
      }
    }
  };

  const currentChat = chats.find(c => c.id === activeChat);

  return (
    <div className={styles.container}>
      <ChatSidebar
        chats={chats}
        activeChat={activeChat}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
        onSettingsClick={() => setIsSettingsOpen(true)}
      />
      <main className={styles.main}>
        <div className={styles.chatHeader}>
          <ThemeToggle />
        </div>
        {currentChat && (
          <ChatContainer
            messages={currentChat.messages}
            onSendMessage={handleSendMessage}
            onFileUpload={handleFileUpload}
          />
        )}
      </main>
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={setSettings}
        initialSettings={settings}
      />
    </div>
  );
}
