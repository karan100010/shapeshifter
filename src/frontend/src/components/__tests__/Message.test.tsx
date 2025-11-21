import { render, screen, fireEvent } from '@testing-library/react';
import Message from '@/components/Message';

describe('Message Component', () => {
    const mockTimestamp = new Date('2024-01-01T12:00:00');

    it('renders user message correctly', () => {
        render(
            <Message
                role="user"
                content="Hello, this is a test message"
                timestamp={mockTimestamp}
            />
        );

        expect(screen.getByText('Hello, this is a test message')).toBeInTheDocument();
        expect(screen.getByText('👤')).toBeInTheDocument();
    });

    it('renders assistant message correctly', () => {
        render(
            <Message
                role="assistant"
                content="I am an AI assistant"
                timestamp={mockTimestamp}
            />
        );

        expect(screen.getByText('I am an AI assistant')).toBeInTheDocument();
        expect(screen.getByText('🤖')).toBeInTheDocument();
    });

    it('displays citations when provided', () => {
        const citations = [
            { source: 'document1.pdf', chunk: 'Page 5' },
            { source: 'document2.pdf', chunk: 'Page 10' },
        ];

        render(
            <Message
                role="assistant"
                content="Here is information from documents"
                timestamp={mockTimestamp}
                citations={citations}
            />
        );

        expect(screen.getByText('📚 Sources:')).toBeInTheDocument();
        expect(screen.getByText('document1.pdf')).toBeInTheDocument();
        expect(screen.getByText('document2.pdf')).toBeInTheDocument();
    });

    it('shows copy button for assistant messages', () => {
        render(
            <Message
                role="assistant"
                content="Test message"
                timestamp={mockTimestamp}
            />
        );

        expect(screen.getByText('📋 Copy')).toBeInTheDocument();
    });

    it('does not show copy button for user messages', () => {
        render(
            <Message
                role="user"
                content="Test message"
                timestamp={mockTimestamp}
            />
        );

        expect(screen.queryByText('📋 Copy')).not.toBeInTheDocument();
    });

    it('copies message to clipboard when copy button is clicked', async () => {
        const writeTextMock = jest.fn();
        Object.assign(navigator, {
            clipboard: {
                writeText: writeTextMock,
            },
        });

        render(
            <Message
                role="assistant"
                content="Copy this text"
                timestamp={mockTimestamp}
            />
        );

        const copyButton = screen.getByText('📋 Copy');
        fireEvent.click(copyButton);

        expect(writeTextMock).toHaveBeenCalledWith('Copy this text');
    });
});
