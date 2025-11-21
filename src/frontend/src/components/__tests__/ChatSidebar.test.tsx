import { render, screen, fireEvent } from '@testing-library/react';
import ChatSidebar from '@/components/ChatSidebar';

const mockChats = [
    { id: '1', title: 'Document Analysis', timestamp: new Date(Date.now() - 3600000) },
    { id: '2', title: 'Query about entities', timestamp: new Date(Date.now() - 7200000) },
    { id: '3', title: 'Graph relationships', timestamp: new Date(Date.now() - 86400000) },
];

describe('ChatSidebar Component', () => {
    it('renders branding and logo', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        expect(screen.getByText('ShapeShifter')).toBeInTheDocument();
        expect(screen.getByText('RAG Assistant')).toBeInTheDocument();
    });

    it('renders new chat button', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        expect(screen.getByText('New Chat')).toBeInTheDocument();
    });

    it('calls onNewChat when new chat button is clicked', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        const newChatButton = screen.getByText('New Chat');
        fireEvent.click(newChatButton);

        expect(mockOnNewChat).toHaveBeenCalledTimes(1);
    });

    it('renders all chats from props', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        expect(screen.getByText('Document Analysis')).toBeInTheDocument();
        expect(screen.getByText('Query about entities')).toBeInTheDocument();
        expect(screen.getByText('Graph relationships')).toBeInTheDocument();
    });

    it('highlights active chat', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="2"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        const chatButtons = screen.getAllByRole('button');
        const activeButton = chatButtons.find(btn => btn.textContent?.includes('Query about entities'));

        expect(activeButton).toHaveClass('active');
    });

    it('calls onChatSelect when chat is clicked', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        const chatButton = screen.getByText('Query about entities');
        fireEvent.click(chatButton);

        expect(mockOnChatSelect).toHaveBeenCalledWith('2');
    });

    it('renders footer buttons', () => {
        const mockOnChatSelect = jest.fn();
        const mockOnNewChat = jest.fn();

        render(
            <ChatSidebar
                chats={mockChats}
                activeChat="1"
                onChatSelect={mockOnChatSelect}
                onNewChat={mockOnNewChat}
            />
        );

        expect(screen.getByText('Settings')).toBeInTheDocument();
        expect(screen.getByText('Documents')).toBeInTheDocument();
    });
});
