from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from config import Config
from utils.helper import load_json_data, save_json_data
from utils.spotify_helper import fetch_audio_features

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load(Config.MODEL_PATH)

def perform_prediction(features_data):
    features = ['danceability', 'energy', 'loudness', 'tempo', 'valence']
    
    # Robustly extract features, falling back to 0.5 (or appropriate middle value) if missing or None
    input_data = []
    for f in features:
        val = features_data.get(f)
        if val is None:
            # Fallback values if Spotify returns None for a feature
            if f == 'loudness':
                val = -10.0
            elif f == 'tempo':
                val = 120.0
            else:
                val = 0.5
        input_data.append(val)
        
    df = pd.DataFrame([input_data], columns=features)
    
    # Get prediction and ensure it's a native Python string
    prediction = model.predict(df)[0]
    prediction = str(prediction)
    
    # Get confidence
    probabilities = model.predict_proba(df)[0]
    confidence = f"{max(probabilities) * 100:.0f}%"
    
    return prediction, confidence

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        prediction, confidence = perform_prediction(data)
        
        # Save to history
        history = load_json_data(Config.DATA_PATH)
        new_entry = {
            "id": len(history) + 1,
            "danceability": data['danceability'],
            "energy": data['energy'],
            "loudness": data['loudness'],
            "tempo": data['tempo'],
            "valence": data['valence'],
            "mood": prediction,
            "confidence": confidence,
            "song_name": data.get('song_name', 'Manual Entry')
        }
        history.append(new_entry)
        save_json_data(Config.DATA_PATH, history)
        
        return jsonify({
            "mood": prediction,
            "confidence": confidence,
            "features": {
                "danceability": data['danceability'],
                "energy": data['energy'],
                "loudness": data['loudness'],
                "tempo": data['tempo'],
                "valence": data['valence']
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/predict-by-name', methods=['POST'])
def predict_by_name():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        song_name = data.get('song_name')
        if not song_name:
            return jsonify({"error": "Song name is required"}), 400

        print(f"DEBUG: Predicting mood for song: {song_name}")
        
        # Fetch features from Spotify
        spotify_data = fetch_audio_features(song_name)
        if "error" in spotify_data:
            print(f"DEBUG: Spotify fetch failed: {spotify_data['error']}")
            return jsonify(spotify_data), 400

        features = spotify_data.get('features')
        if not features:
            print("DEBUG: No features found in Spotify data")
            return jsonify({"error": "Could not extract features for this song."}), 400
            
        prediction, confidence = perform_prediction(features)

        # Save to history
        try:
            history = load_json_data(Config.DATA_PATH)
            new_entry = {
                "id": len(history) + 1,
                **features,
                "mood": prediction,
                "confidence": confidence,
                "song_name": f"{spotify_data.get('song', 'Unknown')} - {spotify_data.get('artist', 'Unknown')}"
            }
            history.append(new_entry)
            save_json_data(Config.DATA_PATH, history)
        except Exception as e:
            print(f"DEBUG: Failed to save history: {e}")
            # We continue even if saving history fails

        return jsonify({
            "mood": prediction,
            "confidence": confidence,
            "song": spotify_data.get('song', 'Unknown'),
            "artist": spotify_data.get('artist', 'Unknown'),
            "features": features,
            "is_demo": spotify_data.get('is_demo', False)
        })
    except Exception as e:
        import traceback
        print(f"DEBUG: Unhandled error in predict_by_name: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
def get_history():
    history = load_json_data(Config.DATA_PATH)
    return jsonify(history)

@app.route('/history', methods=['DELETE'])
def clear_history():
    try:
        save_json_data(Config.DATA_PATH, [])
        return jsonify({"message": "History cleared successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000)
