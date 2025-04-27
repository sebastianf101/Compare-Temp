import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

// Mock the fetch function
global.fetch = jest.fn();

describe('App', () => {
  const mockCities = [
    { id: '1', name: 'City 1' },
    { id: '2', name: 'City 2' },
  ];

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

  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockImplementation((url) => {
      if (url.includes('/api/cities')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockCities),
        });
      }
      if (url.includes('/api/temperature-comparison')) {
        return Promise.resolve({
          json: () => Promise.resolve(mockComparisonData),
        });
      }
      return Promise.reject(new Error('Not found'));
    });
  });

  it('renders the dashboard title', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    expect(screen.getByText('Temperature Comparison Dashboard')).toBeInTheDocument();
  });

  it('fetches and displays cities', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('City 1')).toBeInTheDocument();
      expect(screen.getByText('City 2')).toBeInTheDocument();
    });
  });

  it('handles city selection', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    await waitFor(() => {
      const city1Select = screen.getByLabelText('City 1:');
      fireEvent.change(city1Select, { target: { value: '1' } });
      expect(city1Select.value).toBe('1');
    });
  });

  it('handles date selection', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    const startDateInput = screen.getByLabelText('Start Date:');
    fireEvent.change(startDateInput, { target: { value: '2024-01-01' } });
    expect(startDateInput.value).toBe('2024-01-01');
  });

  it('navigates to results page after comparison', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    await waitFor(() => {
      const city1Select = screen.getByLabelText('City 1:');
      const city2Select = screen.getByLabelText('City 2:');
      fireEvent.change(city1Select, { target: { value: '1' } });
      fireEvent.change(city2Select, { target: { value: '2' } });
    });

    const compareButton = screen.getByRole('button', { name: /compare/i });
    fireEvent.click(compareButton);

    await waitFor(() => {
      expect(screen.getByText('Temperature Comparison Results')).toBeInTheDocument();
    });
  });

  it('displays error message when API call fails', async () => {
    fetch.mockImplementationOnce(() => Promise.reject(new Error('API Error')));

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Failed to load cities')).toBeInTheDocument();
    });
  });
}); 