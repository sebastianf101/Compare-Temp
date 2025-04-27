import React from 'react';

function TemperatureChart({ comparisonData }) {
  if (!comparisonData) return null;

  const maxTemp = Math.max(
    ...comparisonData.hourly_data.map(h => Math.max(h.city1_temperature, h.city2_temperature))
  );
  const minTemp = Math.min(
    ...comparisonData.hourly_data.map(h => Math.min(h.city1_temperature, h.city2_temperature))
  );
  const tempRange = maxTemp - minTemp;

  return (
    <div className="chart-container">
      <div className="chart">
        {comparisonData.hourly_data.map((hour, index) => (
          <div key={index} className="hour-bar">
            <div className="temperature-bars">
              <div
                className="temperature-bar city1"
                style={{
                  height: `${((hour.city1_temperature - minTemp) / tempRange) * 200}px`,
                }}
                title={`City 1: ${hour.city1_temperature}°C`}
              />
              <div
                className="temperature-bar city2"
                style={{
                  height: `${((hour.city2_temperature - minTemp) / tempRange) * 200}px`,
                }}
                title={`City 2: ${hour.city2_temperature}°C`}
              />
            </div>
            <div className="bar-label">{hour.hour}:00</div>
          </div>
        ))}
      </div>
      <div className="summary">
        <div className="min-difference">
          <h3>Minimum Difference</h3>
          <p>Hour: {comparisonData.min_difference.hour}:00</p>
          <p>Difference: {comparisonData.min_difference.difference}°C</p>
        </div>
        <div className="max-difference">
          <h3>Maximum Difference</h3>
          <p>Hour: {comparisonData.max_difference.hour}:00</p>
          <p>Difference: {comparisonData.max_difference.difference}°C</p>
        </div>
      </div>
    </div>
  );
}

export default TemperatureChart; 