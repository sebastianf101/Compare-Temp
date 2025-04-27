import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mock the fetch function
global.fetch = jest.fn();

describe('App', () => {
  const mockCities = [
    { id: 1, name: 'City 1', code: 'C1', latitude: 40.7128, longitude: -74.0060 },
    { id: 2, name: 'City 2', code: 'C2', latitude: 34.0522, longitude: -118.2437 }
  ];

  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockClear();
  });

  it('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders error state when fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch cities'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Error: Failed to fetch cities/)).toBeInTheDocument();
    });
  });

  it('renders cities and date inputs after successful fetch', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockCities)
    });
    
    render(<App />);
    
    await waitFor(() => {
      // Check if city dropdowns are rendered
      expect(screen.getByLabelText('First City:')).toBeInTheDocument();
      expect(screen.getByLabelText('Second City:')).toBeInTheDocument();
      
      // Check if date inputs are rendered
      expect(screen.getByLabelText('Start Date:')).toBeInTheDocument();
      expect(screen.getByLabelText('End Date:')).toBeInTheDocument();
    });
  });

  it('allows selecting cities from dropdowns', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockCities)
    });
    
    render(<App />);
    
    await waitFor(() => {
      const city1Select = screen.getByLabelText('First City:');
      const city2Select = screen.getByLabelText('Second City:');
      
      // Select cities
      fireEvent.change(city1Select, { target: { value: '1' } });
      fireEvent.change(city2Select, { target: { value: '2' } });
      
      expect(city1Select.value).toBe('1');
      expect(city2Select.value).toBe('2');
    });
  });

  it('sets default date range', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockCities)
    });
    
    render(<App />);
    
    await waitFor(() => {
      const startDateInput = screen.getByLabelText('Start Date:');
      const endDateInput = screen.getByLabelText('End Date:');
      
      // Check if dates are set (format: YYYY-MM-DD)
      expect(startDateInput.value).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(endDateInput.value).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });
  });

  it('allows changing date range', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockCities)
    });
    
    render(<App />);
    
    await waitFor(() => {
      const startDateInput = screen.getByLabelText('Start Date:');
      const endDateInput = screen.getByLabelText('End Date:');
      
      // Change dates
      fireEvent.change(startDateInput, { target: { value: '2020-01-01' } });
      fireEvent.change(endDateInput, { target: { value: '2020-12-31' } });
      
      expect(startDateInput.value).toBe('2020-01-01');
      expect(endDateInput.value).toBe('2020-12-31');
    });
  });
}); 