import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
import hashlib
import random

import requests

def get_spotify_client():
    if not Config.SPOTIPY_CLIENT_ID or not Config.SPOTIPY_CLIENT_SECRET:
        print("DEBUG: Spotify credentials missing in .env")
        return None
    
    try:
        # Pre-flight check: Can we reach the accounts server?
        # This prevents the auth_manager from hanging indefinitely if the network blocks it.
        print("DEBUG: Checking Spotify Auth connectivity...")
        requests.get("https://accounts.spotify.com", timeout=3)
        print("DEBUG: Auth connectivity OK.")
        
        print(f"DEBUG: Initializing Spotify client with ID: {Config.SPOTIPY_CLIENT_ID[:5]}...")
        auth_manager = SpotifyClientCredentials(
            client_id=Config.SPOTIPY_CLIENT_ID,
            client_secret=Config.SPOTIPY_CLIENT_SECRET
        )
        
        return spotipy.Spotify(
            auth_manager=auth_manager, 
            requests_timeout=5,
            retries=1
        )
    except Exception as e:
        print(f"DEBUG: Spotify Connectivity/Auth Error: {e}")
        return None

def generate_deterministic_features(seed_string):
    """Generates consistent features for a song based on a seed string (ID or name)."""
    # Create a seed from the string so the same input always has the same features
    seed = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    
    return {
        "danceability": round(rng.uniform(0.3, 0.9), 2),
        "energy": round(rng.uniform(0.3, 0.9), 2),
        "loudness": round(rng.uniform(-15.0, -3.0), 2),
        "tempo": round(rng.uniform(60.0, 180.0), 2),
        "valence": round(rng.uniform(0.1, 0.9), 2)
    }

def fetch_audio_features(song_name):
    """
    Fetches song metadata from Spotify and attempts to get audio features.
    Provides a deep fallback if Spotify is unreachable.
    """
    print(f"DEBUG: fetch_audio_features called for: {song_name}")
    
    # 1. Smart Parsing: Try to extract Artist from "Song - Artist" or "Song by Artist"
    display_song = song_name
    display_artist = "Unknown (API Offline)"
    
    if " - " in song_name:
        parts = song_name.split(" - ", 1)
        display_song = parts[0].strip()
        display_artist = parts[1].strip()
    elif " by " in song_name.lower():
        # Case insensitive split for "by"
        import re
        parts = re.split(r' by ', song_name, flags=re.IGNORECASE)
        display_song = parts[0].strip()
        display_artist = parts[1].strip()

    # Pre-emptively prepare fallback data based on name in case of total failure
    fallback_features = generate_deterministic_features(song_name)
    
    # Simple Keyword Nudging for better "guess" features
    lower_name = song_name.lower()
    if any(word in lower_name for word in ["sad", "lofi", "slow", "cry"]):
        fallback_features["energy"] = round(random.uniform(0.1, 0.3), 2)
        fallback_features["valence"] = round(random.uniform(0.1, 0.3), 2)
        fallback_features["tempo"] = round(random.uniform(60, 90), 2)
    elif any(word in lower_name for word in ["happy", "dance", "party", "pop"]):
        fallback_features["energy"] = round(random.uniform(0.7, 0.9), 2)
        fallback_features["valence"] = round(random.uniform(0.7, 0.9), 2)
        fallback_features["danceability"] = round(random.uniform(0.7, 0.9), 2)
    elif any(word in lower_name for word in ["metal", "rock", "hard", "angry"]):
        fallback_features["energy"] = round(random.uniform(0.8, 1.0), 2)
        fallback_features["valence"] = round(random.uniform(0.1, 0.4), 2)
        fallback_features["loudness"] = round(random.uniform(-5.0, -1.0), 2)

    total_fallback_data = {
        "success": True,
        "song": display_song,
        "artist": display_artist,
        "is_restricted": True,
        "features": fallback_features,
        "note": "Spotify API is currently unreachable. Using generated features."
    }

    sp = get_spotify_client()
    if not sp:
        print("DEBUG: No Spotify client. Using total fallback.")
        return total_fallback_data

    try:
        # 1. Search for the track
        print(f"DEBUG: Searching for track: {song_name}...")
        try:
            results = sp.search(q=song_name, limit=1, type='track')
            print("DEBUG: Search complete.")
        except Exception as search_e:
            print(f"DEBUG: Spotify search failed/timed out: {search_e}. Using total fallback.")
            return total_fallback_data

        items = results.get('tracks', {}).get('items', [])
        if not items:
            return {"success": False, "error": f"Song '{song_name}' not found on Spotify."}

        track = items[0]
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        print(f"DEBUG: Found track: {track_name} by {artist_name} (ID: {track_id})")

        # 2. Attempt to get real audio features
        try:
            print(f"DEBUG: Fetching audio features for ID: {track_id}...")
            features_list = sp.audio_features(track_id)
            print("DEBUG: Audio features fetch complete.")
            if features_list and features_list[0]:
                f = features_list[0]
                return {
                    "success": True,
                    "song": track_name,
                    "artist": artist_name,
                    "is_restricted": False,
                    "features": {
                        "danceability": f['danceability'],
                        "energy": f['energy'],
                        "loudness": f['loudness'],
                        "tempo": f['tempo'],
                        "valence": f['valence']
                    }
                }
        except Exception as api_e:
            print(f"DEBUG: Spotify Audio Features restricted or failed. Error: {api_e}")

        # 3. Fallback: Generate consistent features based on the Spotify Track ID
        print("DEBUG: Using deterministic fallback features (with track ID).")
        features = generate_deterministic_features(track_id)
        return {
            "success": True,
            "song": track_name,
            "artist": artist_name,
            "is_restricted": True,
            "features": features
        }

    except Exception as e:
        print(f"Spotify API Error: {e}. Using total fallback.")
        return total_fallback_data
