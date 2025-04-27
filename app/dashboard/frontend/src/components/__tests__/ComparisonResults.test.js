import React from 'react';
import { render, screen } from '@testing-library/react';
import ComparisonResults from '../ComparisonResults';

describe('ComparisonResults', () => {
  const mockComparisonData = {
    hourly_data: [
      { hour: 0, city1_temperature: 10, city2_temperature: 15 },
      { hour: 6, city1_temperature: 12, city2_temperature: 14 },
    ],
    min_difference: {
      hour: 6,
      difference: 2,
    },
    max_difference: {
      hour: 0,
      difference: 5,
    },
  };

  it('does not render when no comparison data is provided', () => {
    const { container } = render(<ComparisonResults comparisonData={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders the results title', () => {
    render(<ComparisonResults comparisonData={mockComparisonData} />);
    expect(screen.getByText('Temperature Comparison Results')).toBeInTheDocument();
  });

  it('renders the temperature chart', () => {
    render(<ComparisonResults comparisonData={mockComparisonData} />);
    expect(screen.getByTestId('chart-container')).toBeInTheDocument();
  });

  it('passes comparison data to TemperatureChart', () => {
    render(<ComparisonResults comparisonData={mockComparisonData} />);
    expect(screen.getByTestId('chart-container')).toBeInTheDocument();
    expect(screen.getByText('0:00')).toBeInTheDocument();
    expect(screen.getByText('6:00')).toBeInTheDocument();
  });
}); 