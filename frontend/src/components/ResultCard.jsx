import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ResultCard = ({ result }) => {
    if (!result) return null;

    // Define colors for different moods
    const moodColors = {
        happy: '#facc15',    // Yellow
        calm: '#4ade80',     // Green
        sad: '#60a5fa',      // Blue
        energetic: '#f87171', // Light Red
        romantic: '#f472b6', // Pink
        angry: '#ef4444',    // Deep Red
    };

    const currentColor = moodColors[result.mood.toLowerCase()] || '#38bdf8';

    // Prepare data for the graph
    const chartData = [
        { name: 'Danceability', value: result.features?.danceability || 0 },
        { name: 'Energy', value: result.features?.energy || 0 },
        { name: 'Valence', value: result.features?.valence || 0 },
        { name: 'Tempo (Scaled)', value: (result.features?.tempo || 0) / 200 }, // Scale tempo to 0-1 range
        { name: 'Loudness (Scaled)', value: (result.features?.loudness + 60) / 60 }, // Scale loudness to 0-1 range
    ];

    return (
        <div className="result-card">
            <h3>Prediction Result</h3>
            {result.song && (
                <div className="song-info">
                    <p><strong>{result.song}</strong> by {result.artist}</p>
                    {result.is_demo && <small className="demo-tag"> (Demo Data)</small>}
                </div>
            )}
            
            <div className="result-main">
                <div className="result-text">
                    <div className="mood-display">
                        <span className="mood-label">Predicted Mood:</span>
                        <span className={`mood-value ${result.mood.toLowerCase()}`}>{result.mood}</span>
                    </div>
                    <div className="confidence-display">
                        <span className="confidence-label">Confidence:</span>
                        <span className="confidence-value">{result.confidence}</span>
                    </div>
                </div>

                <div className="chart-container" style={{ width: '100%', height: 250, marginTop: '20px' }}>
                    <ResponsiveContainer>
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis 
                                dataKey="name" 
                                stroke="#94a3b8" 
                                fontSize={10} 
                                interval={0} 
                            />
                            <YAxis stroke="#94a3b8" fontSize={10} domain={[0, 1]} />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                itemStyle={{ color: currentColor }}
                            />
                            <Line 
                                type="monotone" 
                                dataKey="value" 
                                stroke={currentColor} 
                                strokeWidth={3} 
                                dot={{ fill: currentColor, r: 6 }} 
                                activeDot={{ r: 8 }}
                                animationDuration={1000}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default ResultCard;
