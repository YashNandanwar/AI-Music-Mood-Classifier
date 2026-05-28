import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train():
    # Get the directory where this file is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Load dataset
    data_path = os.path.join(BASE_DIR, '..', 'dataset', 'music_dataset.csv')
    df = pd.read_csv(data_path)

    # Features and target
    X = df[['danceability', 'energy', 'loudness', 'tempo', 'valence']]
    y = df['mood']

    # Initialize and train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    model_dir = os.path.join(BASE_DIR, 'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'mood_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model trained and saved successfully at {model_path}")

if __name__ == "__main__":
    train()
