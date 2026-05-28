# AI Music Mood Classifier Architecture

## Overview
This application uses a Random Forest Classifier to predict the mood of a song based on its audio features.

## Components
1. **Frontend**: React + Vite application.
2. **Backend**: Flask REST API.
3. **Machine Learning Model**: Scikit-learn Random Forest model.
4. **Storage**: JSON file (`songs.json`) for persistence.

## Data Flow
1. User enters audio features (Danceability, Energy, etc.) in the React form.
2. React app sends a POST request to `/predict`.
3. Flask app receives the request and passes the data to the ML model.
4. ML model returns the predicted mood and confidence.
5. Flask app saves the entry to `songs.json`.
6. Flask app returns the prediction result to the React app.
7. React app displays the result and updates the history.
