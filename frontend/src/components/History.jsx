import React from 'react';

const History = ({ history, onClearHistory }) => {
    return (
        <div id="history" className="history-panel">
            <div className="history-header">
                <h3>Prediction History</h3>
                {history.length > 0 && (
                    <button className="clear-btn" onClick={onClearHistory}>
                        Clear History
                    </button>
                )}
            </div>
            <div className="history-table-container">
                <table className="history-table">
                    <thead>
                        <tr>
                            <th>Song</th>
                            <th>Dance</th>
                            <th>Energy</th>
                            <th>Mood</th>
                            <th>Conf.</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.slice().reverse().map((item) => (
                            <tr key={item.id}>
                                <td>{item.song_name || 'Manual'}</td>
                                <td>{item.danceability.toFixed(2)}</td>
                                <td>{item.energy.toFixed(2)}</td>
                                <td className={`mood-${item.mood.toLowerCase()}`}>{item.mood}</td>
                                <td>{item.confidence}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default History;
