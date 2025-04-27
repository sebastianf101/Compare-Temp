import React from 'react';
import TemperatureChart from './TemperatureChart';

function ComparisonResults({ comparisonData }) {
  if (!comparisonData) return null;

  return (
    <div className="comparison-results">
      <h2>Temperature Comparison Results</h2>
      <TemperatureChart comparisonData={comparisonData} />
    </div>
  );
}

export default ComparisonResults; 