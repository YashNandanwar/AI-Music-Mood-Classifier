import React, { useState } from 'react';

const MoodForm = ({ onPredict, onPredictByName }) => {
    const [isManual, setIsManual] = useState(false);
    const [songName, setSongName] = useState('');
    const [formData, setFormData] = useState({
        danceability: 0.5,
        energy: 0.5,
        loudness: -10,
        tempo: 120,
        valence: 0.5
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: parseFloat(value)
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isManual) {
            onPredict(formData);
        } else {
            onPredictByName(songName);
        }
    };

    return (
        <div className="mood-form-container">
            <div className="mode-selector">
                <button 
                    className={`mode-btn ${!isManual ? 'active' : ''}`} 
                    onClick={() => setIsManual(false)}
                >
                    Search by Name
                </button>
                <button 
                    className={`mode-btn ${isManual ? 'active' : ''}`} 
                    onClick={() => setIsManual(true)}
                >
                    Manual Features
                </button>
            </div>

            <form className="mood-form" onSubmit={handleSubmit}>
                {!isManual ? (
                    <div className="form-group">
                        <label>Song Name</label>
                        <input 
                            type="text" 
                            placeholder="e.g. Blinding Lights" 
                            value={songName} 
                            onChange={(e) => setSongName(e.target.value)}
                            required
                        />
                    </div>
                ) : (
                    <>
                        <div className="form-group">
                            <label>Danceability (0 to 1)</label>
                            <input type="number" step="0.01" min="0" max="1" name="danceability" value={formData.danceability} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Energy (0 to 1)</label>
                            <input type="number" step="0.01" min="0" max="1" name="energy" value={formData.energy} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Loudness (-60 to 0 dB)</label>
                            <input type="number" step="0.1" min="-60" max="0" name="loudness" value={formData.loudness} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Tempo (BPM)</label>
                            <input type="number" name="tempo" value={formData.tempo} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Valence (0 to 1)</label>
                            <input type="number" step="0.01" min="0" max="1" name="valence" value={formData.valence} onChange={handleChange} />
                        </div>
                    </>
                )}
                <button type="submit" className="btn-predict">
                    {isManual ? 'Predict Mood' : 'Search & Predict'}
                </button>
            </form>
        </div>
    );
};

export default MoodForm;
