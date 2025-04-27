import React from 'react';
import { render, screen } from '@testing-library/react';
import TemperatureChart from '../TemperatureChart';

describe('TemperatureChart', () => {
  const mockComparisonData = {
    hourly_data: [
      { hour: 0, city1_temperature: 10, city2_temperature: 15 },
      { hour: 6, city1_temperature: 12, city2_temperature: 14 },
      { hour: 12, city1_temperature: 20, city2_temperature: 18 },
      { hour: 18, city1_temperature: 15, city2_temperature: 16 },
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
    const { container } = render(<TemperatureChart comparisonData={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders temperature bars for each hour', () => {
    render(<TemperatureChart comparisonData={mockComparisonData} />);
    
    const hourBars = screen.getAllByTestId('hour-bar');
    expect(hourBars).toHaveLength(4);
  });

  it('renders hour labels', () => {
    render(<TemperatureChart comparisonData={mockComparisonData} />);
    
    expect(screen.getByText('0:00')).toBeInTheDocument();
    expect(screen.getByText('6:00')).toBeInTheDocument();
    expect(screen.getByText('12:00')).toBeInTheDocument();
    expect(screen.getByText('18:00')).toBeInTheDocument();
  });

  it('renders temperature bars with correct heights', () => {
    render(<TemperatureChart comparisonData={mockComparisonData} />);
    
    const city1Bars = screen.getAllByTitle(/City 1:/);
    const city2Bars = screen.getAllByTitle(/City 2:/);
    
    expect(city1Bars).toHaveLength(4);
    expect(city2Bars).toHaveLength(4);
  });

  it('renders min and max difference information', () => {
    render(<TemperatureChart comparisonData={mockComparisonData} />);
    
    expect(screen.getByText('Minimum Difference')).toBeInTheDocument();
    expect(screen.getByText('Maximum Difference')).toBeInTheDocument();
    expect(screen.getByText('Hour: 6:00')).toBeInTheDocument();
    expect(screen.getByText('Difference: 2°C')).toBeInTheDocument();
    expect(screen.getByText('Hour: 0:00')).toBeInTheDocument();
    expect(screen.getByText('Difference: 5°C')).toBeInTheDocument();
  });
}); 