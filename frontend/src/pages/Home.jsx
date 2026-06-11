import React, { useState, useEffect } from 'react';
import MoodForm from '../components/MoodForm';
import ResultCard from '../components/ResultCard';
import History from '../components/History';
import { predictMoodByName, getHistory, clearHistory } from '../services/api';

const Home = () => {
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
    const [mobileStep, setMobileStep] = useState(1); // 1: Search, 2: Result

    useEffect(() => {
        const handleResize = () => {
            const mobile = window.innerWidth <= 768;
            setIsMobile(mobile);
            // Reset to step 1 if we switch from desktop to mobile to be safe,
            // or if it's already desktop, steps don't matter.
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

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

    const handlePredictByName = async (songName) => {
        setLoading(true);
        if (isMobile) {
            setMobileStep(2);
        }
        try {
            const data = await predictMoodByName(songName);
            setResult(data);
            fetchHistory();
        } catch (error) {
            console.error('Prediction error:', error);
            const msg = error.response?.data?.error || 
                        error.message || 
                        'Error predicting mood by name. Please check if the backend is running.';
            alert(msg);
            if (isMobile) {
                setMobileStep(1); // Go back if error occurs on mobile
            }
        } finally {
            setLoading(false);
        }
    };

    const renderMobileView = () => {
        if (mobileStep === 1) {
            return (
                <div className="form-section">
                    <MoodForm onPredictByName={handlePredictByName} />
                </div>
            );
        } else {
            return (
                <div className="results-section mobile-results">
                    {loading ? (
                        <div className="loading-container">
                            <p className="loading-text">Analyzing Song Features...</p>
                        </div>
                    ) : (
                        <>
                            <ResultCard result={result} />
                            <History history={history} onClearHistory={handleClearHistory} />
                        </>
                    )}
                    <button 
                        className="back-btn mobile-bottom-back" 
                        onClick={() => setMobileStep(1)}
                    >
                        ← Back to Search
                    </button>
                </div>
            );
        }
    };

    return (
        <main className="home-page">
            <div className="hero">
                <h2 className="hero-title">Analyze Your Music Mood</h2>
                <p>Discover the emotional vibe of any song using AI.</p>
            </div>
            
            <div className="main-content container">
                {isMobile ? (
                    renderMobileView()
                ) : (
                    <>
                        <div className="form-section">
                            <MoodForm onPredictByName={handlePredictByName} />
                        </div>
                        <div className="results-section">
                            {loading ? <p className="loading-text">Analyzing Song Features...</p> : <ResultCard result={result} />}
                            <History history={history} onClearHistory={handleClearHistory} />
                        </div>
                    </>
                )}
            </div>
        </main>
    );
};

export default Home;
