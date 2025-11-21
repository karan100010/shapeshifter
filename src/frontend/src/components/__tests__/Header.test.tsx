import { render, screen } from '@testing-library/react';
import Header from '@/components/Header';
import { ThemeProvider } from '@/contexts/ThemeContext';

const renderWithTheme = (component: React.ReactElement) => {
    return render(<ThemeProvider>{component}</ThemeProvider>);
};

describe('Header Component', () => {
    it('renders the header', () => {
        renderWithTheme(<Header />);
        expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
    });

    it('renders search input', () => {
        renderWithTheme(<Header />);
        const searchInput = screen.getByPlaceholderText('Search...');
        expect(searchInput).toBeInTheDocument();
        expect(searchInput).toHaveAttribute('type', 'text');
    });

    it('renders notification button with badge', () => {
        renderWithTheme(<Header />);
        expect(screen.getByText('🔔')).toBeInTheDocument();
        expect(screen.getByText('3')).toBeInTheDocument(); // Badge count
    });

    it('renders user profile section', () => {
        renderWithTheme(<Header />);
        expect(screen.getByText('Kunal')).toBeInTheDocument();
        expect(screen.getByText('K')).toBeInTheDocument(); // Avatar
    });

    it('renders search icon', () => {
        renderWithTheme(<Header />);
        expect(screen.getByText('🔍')).toBeInTheDocument();
    });
});
