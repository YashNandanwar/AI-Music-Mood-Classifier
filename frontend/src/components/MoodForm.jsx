import React, { useState } from 'react';

const MoodForm = ({ onPredictByName }) => {
    const [songName, setSongName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onPredictByName(songName);
    };

    return (
        <div className="mood-form-container">
            <form className="mood-form" onSubmit={handleSubmit}>
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
                <button type="submit" className="btn-predict">
                    Search & Predict Mood
                </button>

            </form>
        </div>
    );
};

export default MoodForm;
