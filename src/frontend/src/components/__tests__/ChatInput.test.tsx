import { render, screen, fireEvent } from '@testing-library/react';
import ChatInput from '@/components/ChatInput';

describe('ChatInput Component', () => {
    it('renders input field and send button', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        expect(screen.getByPlaceholderText('Ask me anything about your documents...')).toBeInTheDocument();
        expect(screen.getByLabelText('Send message')).toBeInTheDocument();
    });

    it('renders query suggestions', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        expect(screen.getByText(/What documents are available/i)).toBeInTheDocument();
        expect(screen.getByText(/Explain the main concepts/i)).toBeInTheDocument();
        expect(screen.getByText(/Summarize the key findings/i)).toBeInTheDocument();
    });

    it('calls onSend when send button is clicked', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...');
        fireEvent.change(input, { target: { value: 'Test message' } });

        const sendButton = screen.getByLabelText('Send message');
        fireEvent.click(sendButton);

        expect(mockOnSend).toHaveBeenCalledWith('Test message');
    });

    it('clears input after sending message', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...') as HTMLTextAreaElement;
        fireEvent.change(input, { target: { value: 'Test message' } });

        const sendButton = screen.getByLabelText('Send message');
        fireEvent.click(sendButton);

        expect(input.value).toBe('');
    });

    it('disables send button when input is empty', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        const sendButton = screen.getByLabelText('Send message') as HTMLButtonElement;
        expect(sendButton.disabled).toBe(true);
    });

    it('enables send button when input has text', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...');
        fireEvent.change(input, { target: { value: 'Test' } });

        const sendButton = screen.getByLabelText('Send message') as HTMLButtonElement;
        expect(sendButton.disabled).toBe(false);
    });

    it('fills input when suggestion is clicked', () => {
        const mockOnSend = jest.fn();
        render(<ChatInput onSend={mockOnSend} />);

        const suggestion = screen.getByText(/What documents are available/i);
        fireEvent.click(suggestion);

        const input = screen.getByPlaceholderText('Ask me anything about your documents...') as HTMLTextAreaElement;
        expect(input.value).toBe('What documents are available?');
    });
});
