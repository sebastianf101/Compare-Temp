import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SelectionPanel from '../SelectionPanel';

describe('SelectionPanel', () => {
  const mockCities = [
    { id: '1', name: 'City 1' },
    { id: '2', name: 'City 2' },
    { id: '3', name: 'City 3' },
  ];

  const defaultProps = {
    cities: mockCities,
    selectedCity1: '',
    selectedCity2: '',
    startDate: '2024-01-01',
    endDate: '2024-01-07',
    onCityChange: jest.fn(),
    onDateChange: jest.fn(),
    onCompare: jest.fn(),
    loading: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders city selection dropdowns', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    expect(screen.getByLabelText('City 1:')).toBeInTheDocument();
    expect(screen.getByLabelText('City 2:')).toBeInTheDocument();
  });

  it('renders date selection inputs', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    expect(screen.getByLabelText('Start Date:')).toBeInTheDocument();
    expect(screen.getByLabelText('End Date:')).toBeInTheDocument();
  });

  it('renders compare button', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    expect(screen.getByRole('button', { name: /compare/i })).toBeInTheDocument();
  });

  it('calls onCityChange when city is selected', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    const city1Select = screen.getByLabelText('City 1:');
    fireEvent.change(city1Select, { target: { value: '1' } });
    
    expect(defaultProps.onCityChange).toHaveBeenCalledWith('city1', '1');
  });

  it('calls onDateChange when date is changed', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    const startDateInput = screen.getByLabelText('Start Date:');
    fireEvent.change(startDateInput, { target: { value: '2024-01-02' } });
    
    expect(defaultProps.onDateChange).toHaveBeenCalledWith('start', '2024-01-02');
  });

  it('calls onCompare when compare button is clicked', () => {
    render(<SelectionPanel {...defaultProps} />);
    
    const compareButton = screen.getByRole('button', { name: /compare/i });
    fireEvent.click(compareButton);
    
    expect(defaultProps.onCompare).toHaveBeenCalled();
  });

  it('disables compare button when loading', () => {
    render(<SelectionPanel {...defaultProps} loading={true} />);
    
    const compareButton = screen.getByRole('button', { name: /loading/i });
    expect(compareButton).toBeDisabled();
  });

  it('shows loading text on button when loading', () => {
    render(<SelectionPanel {...defaultProps} loading={true} />);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
}); 