import { render, screen } from '@testing-library/react';
import Header from '@/components/Header';

describe('Header Component', () => {
    it('renders the header', () => {
        render(<Header />);
        expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
    });

    it('renders search input', () => {
        render(<Header />);
        const searchInput = screen.getByPlaceholderText('Search...');
        expect(searchInput).toBeInTheDocument();
        expect(searchInput).toHaveAttribute('type', 'text');
    });

    it('renders notification button with badge', () => {
        render(<Header />);
        expect(screen.getByText('🔔')).toBeInTheDocument();
        expect(screen.getByText('3')).toBeInTheDocument(); // Badge count
    });

    it('renders user profile section', () => {
        render(<Header />);
        expect(screen.getByText('Kunal')).toBeInTheDocument();
        expect(screen.getByText('K')).toBeInTheDocument(); // Avatar
    });

    it('renders search icon', () => {
        render(<Header />);
        expect(screen.getByText('🔍')).toBeInTheDocument();
    });
});
