import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatContainer from '@/components/ChatContainer';

const mockMessages = [
    {
        id: '1',
        role: 'assistant' as const,
        content: 'Hello! I\'m your RAG assistant. I can help you query documents, find information, and answer questions based on your knowledge base. How can I help you today?',
        timestamp: new Date(),
    }
];

describe('ChatContainer Component', () => {
    beforeEach(() => {
        // Mock scrollIntoView
        Element.prototype.scrollIntoView = jest.fn();
    });

    it('renders initial welcome message', () => {
        const mockOnSend = jest.fn();
        render(<ChatContainer chatId="1" messages={mockMessages} onSendMessage={mockOnSend} />);

        expect(screen.getByText(/Hello! I'm your RAG assistant/i)).toBeInTheDocument();
    });

    it('displays typing indicator when last message is from user', () => {
        const mockOnSend = jest.fn();
        const messagesWithUser = [
            ...mockMessages,
            {
                id: '2',
                role: 'user' as const,
                content: 'Test query',
                timestamp: new Date(),
            }
        ];

        render(<ChatContainer chatId="1" messages={messagesWithUser} onSendMessage={mockOnSend} />);

        // Check for typing indicator by class
        const typingIndicator = document.querySelector('.typingIndicator');
        expect(typingIndicator).toBeInTheDocument();
    });

    it('adds user message when sent', () => {
        const mockOnSend = jest.fn();
        render(<ChatContainer chatId="1" messages={mockMessages} onSendMessage={mockOnSend} />);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...');
        const sendButton = screen.getByLabelText('Send message');

        fireEvent.change(input, { target: { value: 'My test message' } });
        fireEvent.click(sendButton);

        expect(mockOnSend).toHaveBeenCalledWith('My test message');
    });

    it('displays all messages from props', () => {
        const mockOnSend = jest.fn();
        const multipleMessages = [
            ...mockMessages,
            {
                id: '2',
                role: 'user' as const,
                content: 'Test query',
                timestamp: new Date(),
            },
            {
                id: '3',
                role: 'assistant' as const,
                content: 'Test response',
                timestamp: new Date(),
            }
        ];

        render(<ChatContainer chatId="1" messages={multipleMessages} onSendMessage={mockOnSend} />);

        expect(screen.getByText(/Hello! I'm your RAG assistant/i)).toBeInTheDocument();
        expect(screen.getByText('Test query')).toBeInTheDocument();
        expect(screen.getByText('Test response')).toBeInTheDocument();
    });

    it('disables input when typing indicator is shown', () => {
        const mockOnSend = jest.fn();
        const messagesWithUser = [
            ...mockMessages,
            {
                id: '2',
                role: 'user' as const,
                content: 'Test',
                timestamp: new Date(),
            }
        ];

        render(<ChatContainer chatId="1" messages={messagesWithUser} onSendMessage={mockOnSend} />);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...');
        expect(input).toBeDisabled();
    });

    it('scrolls to bottom when messages change', () => {
        const scrollIntoViewMock = jest.fn();
        Element.prototype.scrollIntoView = scrollIntoViewMock;

        const mockOnSend = jest.fn();
        const { rerender } = render(<ChatContainer chatId="1" messages={mockMessages} onSendMessage={mockOnSend} />);

        const newMessages = [
            ...mockMessages,
            {
                id: '2',
                role: 'user' as const,
                content: 'New message',
                timestamp: new Date(),
            }
        ];

        rerender(<ChatContainer chatId="1" messages={newMessages} onSendMessage={mockOnSend} />);

        expect(scrollIntoViewMock).toHaveBeenCalled();
    });
});
