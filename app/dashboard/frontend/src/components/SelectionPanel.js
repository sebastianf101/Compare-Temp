import React from 'react';

function SelectionPanel({ cities, selectedCity1, selectedCity2, startDate, endDate, onCityChange, onDateChange, onCompare, loading }) {
  return (
    <div className="selection-container">
      <div className="city-selection">
        <label>
          City 1:
          <select value={selectedCity1} onChange={e => onCityChange('city1', e.target.value)}>
            <option value="">Select a city</option>
            {cities.map(city => (
              <option key={city.id} value={city.id}>{city.name}</option>
            ))}
          </select>
        </label>
        <label>
          City 2:
          <select value={selectedCity2} onChange={e => onCityChange('city2', e.target.value)}>
            <option value="">Select a city</option>
            {cities.map(city => (
              <option key={city.id} value={city.id}>{city.name}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="date-selection">
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={e => onDateChange('start', e.target.value)}
          />
        </label>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={e => onDateChange('end', e.target.value)}
          />
        </label>
      </div>
      <button onClick={onCompare} disabled={loading}>
        {loading ? 'Loading...' : 'Compare'}
      </button>
    </div>
  );
}

export default SelectionPanel; 