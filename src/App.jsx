
import React from 'react';
import Plot from 'react-plotly.js';

const forecastData = {
  x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  gru: [4.2, 4.4, 4.1, 4.6, 4.3, 4.5, 4.7],
  lstm: [4.1, 4.3, 4.0, 4.4, 4.2, 4.4, 4.6]
};

const clusterData = [
  { label: 'Low Users', color: 'green', count: 6 },
  { label: 'Avg Users', color: 'orange', count: 8 },
  { label: 'High Users', color: 'red', count: 3 }
];

export default function App() {
  return (
    <div className="dashboard">
      <h1>DSM+SAT Pro – Phase 2: Forecasting + Clustering</h1>

      <div className="section">
        <h2>📈 Forecasting (GRU vs LSTM)</h2>
        <Plot
          data={[
            { x: forecastData.x, y: forecastData.gru, type: 'scatter', mode: 'lines+markers', name: 'GRU' },
            { x: forecastData.x, y: forecastData.lstm, type: 'scatter', mode: 'lines+markers', name: 'LSTM' }
          ]}
          layout={{ paper_bgcolor: '#1a1a1a', plot_bgcolor: '#1a1a1a', font: { color: 'white' }, title: 'Weekly Energy Forecast (kWh)' }}
        />
      </div>

      <div className="section">
        <h2>🔀 Clustering</h2>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {clusterData.map((c, i) => (
            <div key={i} style={{ backgroundColor: c.color, padding: '1rem', borderRadius: '8px', minWidth: '120px' }}>
              <strong>{c.label}</strong><br />
              Households: {c.count}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
