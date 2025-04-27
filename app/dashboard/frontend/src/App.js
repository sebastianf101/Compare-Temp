import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import SelectionPanel from './components/SelectionPanel';
import ComparisonResults from './components/ComparisonResults';

function App() {
  const [cities, setCities] = useState([]);
  const [selectedCity1, setSelectedCity1] = useState('');
  const [selectedCity2, setSelectedCity2] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comparisonData, setComparisonData] = useState(null);

  useEffect(() => {
    // Set default date range (last 7 days)
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 7);
    setStartDate(start.toISOString().split('T')[0]);
    setEndDate(end.toISOString().split('T')[0]);

    // Fetch cities
    fetch('/api/cities')
      .then(response => response.json())
      .then(data => setCities(data))
      .catch(err => setError('Failed to load cities'));
  }, []);

  const handleCityChange = (cityType, value) => {
    if (cityType === 'city1') {
      setSelectedCity1(value);
    } else {
      setSelectedCity2(value);
    }
  };

  const handleDateChange = (dateType, value) => {
    if (dateType === 'start') {
      setStartDate(value);
    } else {
      setEndDate(value);
    }
  };

  const handleCompare = () => {
    if (!selectedCity1 || !selectedCity2 || !startDate || !endDate) {
      setError('Please select both cities and date range');
      return;
    }

    setLoading(true);
    setError(null);

    fetch(`/api/temperature-comparison?city1_id=${selectedCity1}&city2_id=${selectedCity2}&start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
        setComparisonData(data);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to fetch comparison data');
        setLoading(false);
      });
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Temperature Comparison Dashboard</h1>
        </header>
        <main className="App-main">
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <SelectionPanel
                    cities={cities}
                    selectedCity1={selectedCity1}
                    selectedCity2={selectedCity2}
                    startDate={startDate}
                    endDate={endDate}
                    onCityChange={handleCityChange}
                    onDateChange={handleDateChange}
                    onCompare={handleCompare}
                    loading={loading}
                  />
                  {error && <div className="error">{error}</div>}
                  {comparisonData && <Navigate to="/results" replace />}
                </>
              }
            />
            <Route
              path="/results"
              element={
                <>
                  <SelectionPanel
                    cities={cities}
                    selectedCity1={selectedCity1}
                    selectedCity2={selectedCity2}
                    startDate={startDate}
                    endDate={endDate}
                    onCityChange={handleCityChange}
                    onDateChange={handleDateChange}
                    onCompare={handleCompare}
                    loading={loading}
                  />
                  {error && <div className="error">{error}</div>}
                  <ComparisonResults comparisonData={comparisonData} />
                </>
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 