import React, { useState, useEffect } from 'react';
import MoodForm from '../components/MoodForm';
import ResultCard from '../components/ResultCard';
import History from '../components/History';
import { predictMood, predictMoodByName, getHistory, clearHistory } from '../services/api';

const Home = () => {
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await getHistory();
            setHistory(data);
        } catch (error) {
            console.error('Failed to fetch history');
        }
    };

    const handleClearHistory = async () => {
        if (window.confirm('Are you sure you want to clear all history?')) {
            try {
                await clearHistory();
                setHistory([]);
            } catch (error) {
                alert('Failed to clear history');
            }
        }
    };

    const handlePredict = async (formData) => {
        setLoading(true);
        try {
            const data = await predictMood(formData);
            setResult(data);
            fetchHistory();
        } catch (error) {
            alert('Error predicting mood. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    const handlePredictByName = async (songName) => {
        setLoading(true);
        try {
            const data = await predictMoodByName(songName);
            setResult(data);
            fetchHistory();
        } catch (error) {
            const msg = error.response?.data?.error || 'Error predicting mood by name.';
            alert(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="home-page">
            <div className="hero">
                <h2>Analyze Your Music Mood</h2>
                <p>Discover the emotional vibe of any song using AI.</p>
            </div>
            <div className="main-content container">
                <div className="form-section">
                    <MoodForm onPredict={handlePredict} onPredictByName={handlePredictByName} />
                </div>
                <div className="results-section">
                    {loading ? <p className="loading-text">Analyzing Song Features...</p> : <ResultCard result={result} />}
                    <History history={history} onClearHistory={handleClearHistory} />
                </div>
            </div>
        </main>
    );
};

export default Home;
