import { render, screen } from '@testing-library/react';
import StatsWidget from '@/components/StatsWidget';

describe('StatsWidget Component', () => {
    it('renders widget with title and value', () => {
        render(
            <StatsWidget
                title="Total Documents"
                value="1,234"
                icon="📄"
            />
        );
        expect(screen.getByText('TOTAL DOCUMENTS')).toBeInTheDocument();
        expect(screen.getByText('1,234')).toBeInTheDocument();
        expect(screen.getByText('📄')).toBeInTheDocument();
    });

    it('renders widget with positive change', () => {
        render(
            <StatsWidget
                title="Active Queries"
                value="89"
                change="+12.5%"
                icon="🔍"
                trend="up"
            />
        );
        expect(screen.getByText('+12.5%')).toBeInTheDocument();
        expect(screen.getByText('↑')).toBeInTheDocument();
    });

    it('renders widget with negative change', () => {
        render(
            <StatsWidget
                title="Graph Nodes"
                value="5,678"
                change="-2.1%"
                icon="🕸️"
                trend="down"
            />
        );
        expect(screen.getByText('-2.1%')).toBeInTheDocument();
        expect(screen.getByText('↓')).toBeInTheDocument();
    });

    it('renders widget without change indicator', () => {
        render(
            <StatsWidget
                title="API Calls"
                value="12.4K"
                icon="⚡"
            />
        );
        expect(screen.getByText('API CALLS')).toBeInTheDocument();
        expect(screen.getByText('12.4K')).toBeInTheDocument();
        // Should not have change indicator
        expect(screen.queryByText('↑')).not.toBeInTheDocument();
        expect(screen.queryByText('↓')).not.toBeInTheDocument();
    });

    it('applies correct CSS class for upward trend', () => {
        const { container } = render(
            <StatsWidget
                title="Test"
                value="100"
                change="+10%"
                icon="📊"
                trend="up"
            />
        );
        const changeElement = screen.getByText('+10%').parentElement;
        expect(changeElement).toHaveClass('up');
    });

    it('applies correct CSS class for downward trend', () => {
        const { container } = render(
            <StatsWidget
                title="Test"
                value="100"
                change="-10%"
                icon="📊"
                trend="down"
            />
        );
        const changeElement = screen.getByText('-10%').parentElement;
        expect(changeElement).toHaveClass('down');
    });
});
