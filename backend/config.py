import os
from dotenv import load_dotenv

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    MODEL_PATH = os.path.join(BASE_DIR, 'model', 'mood_model.pkl')
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'songs.json')
    DEBUG = True
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    
    # Debug print (will show in terminal when you start app.py)
    if not SPOTIPY_CLIENT_ID:
        print("DEBUG: SPOTIPY_CLIENT_ID is MISSING")
    else:
        print(f"DEBUG: SPOTIPY_CLIENT_ID loaded (starts with {SPOTIPY_CLIENT_ID[:5]}...)")
