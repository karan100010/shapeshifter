import { render, screen } from '@testing-library/react';
import Sidebar from '@/components/Sidebar';

import { usePathname } from 'next/navigation';

// Mock usePathname from next/navigation
jest.mock('next/navigation', () => ({
    usePathname: jest.fn(),
}));

describe('Sidebar Component', () => {
    beforeEach(() => {
        (usePathname as jest.Mock).mockReturnValue('/dashboard');
    });

    it('renders the sidebar with logo', () => {
        render(<Sidebar />);
        expect(screen.getByText('ShapeShifter')).toBeInTheDocument();
    });

    it('renders all navigation items', () => {
        render(<Sidebar />);
        expect(screen.getByText('Dashboard')).toBeInTheDocument();
        expect(screen.getByText('Analytics')).toBeInTheDocument();
        expect(screen.getByText('Documents')).toBeInTheDocument();
        expect(screen.getByText('Settings')).toBeInTheDocument();
    });

    it('highlights the active navigation item', () => {
        render(<Sidebar />);
        const dashboardLink = screen.getByText('Dashboard').closest('a');
        expect(dashboardLink).toHaveClass('active');
    });

    it('renders navigation icons', () => {
        render(<Sidebar />);
        // Check if icons are present (emojis)
        expect(screen.getByText('📊')).toBeInTheDocument();
        expect(screen.getByText('📈')).toBeInTheDocument();
        expect(screen.getByText('📄')).toBeInTheDocument();
        expect(screen.getByText('⚙️')).toBeInTheDocument();
    });
});
