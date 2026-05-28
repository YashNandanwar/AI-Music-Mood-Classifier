import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
import random

def get_spotify_client():
    if not Config.SPOTIPY_CLIENT_ID or not Config.SPOTIPY_CLIENT_SECRET:
        return None
    
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=Config.SPOTIPY_CLIENT_ID,
            client_secret=Config.SPOTIPY_CLIENT_SECRET
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"Spotify Auth Error: {e}")
        return None

def get_mock_features(song_name):
    """Generates realistic random features for testing when API is unavailable."""
    return {
        "success": True,
        "is_demo": True,
        "song": song_name.title(),
        "artist": "Demo Artist",
        "features": {
            "danceability": round(random.uniform(0.3, 0.9), 2),
            "energy": round(random.uniform(0.3, 0.9), 2),
            "loudness": round(random.uniform(-15.0, -3.0), 2),
            "tempo": round(random.uniform(60.0, 180.0), 2),
            "valence": round(random.uniform(0.1, 0.9), 2)
        }
    }

def fetch_audio_features(song_name):
    sp = get_spotify_client()
    
    # If no credentials or auth failed, use mock data immediately
    if not sp:
        print("DEBUG: No Spotify credentials, using Mock Fallback.")
        return get_mock_features(song_name)

    try:
        # Search for the track
        results = sp.search(q=song_name, limit=1, type='track')
        items = results.get('tracks', {}).get('items', [])
        
        if not items:
            print(f"DEBUG: Song '{song_name}' not found on Spotify, using Mock Fallback.")
            return get_mock_features(song_name)

        track = items[0]
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # Get audio features
        features_list = sp.audio_features(track_id)
        if not features_list or not features_list[0]:
            print(f"DEBUG: Could not retrieve audio features for '{song_name}', using Mock Fallback.")
            return get_mock_features(song_name)

        f = features_list[0]
        return {
            "success": True,
            "is_demo": False,
            "song": track_name,
            "artist": artist_name,
            "features": {
                "danceability": f['danceability'],
                "energy": f['energy'],
                "loudness": f['loudness'],
                "tempo": f['tempo'],
                "valence": f['valence']
            }
        }
    except Exception as e:
        error_msg = str(e).lower()
        print(f"DEBUG: Spotify API Error: {error_msg}")
        
        # Broad fallback: If anything goes wrong with the API (auth, 403, 401, network, etc.), use mock data.
        # This ensures the app always provides a result for the user.
        print(f"DEBUG: Switching to Mock Fallback for song '{song_name}' due to: {error_msg}")
        return get_mock_features(song_name)
