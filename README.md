# AI Music Mood Classifier

Predict song moods using Machine Learning.

## Setup

### Backend
1. Go to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Spotify:
   - Create a `.env` file in the `backend/` folder.
   - Add your `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` from the Spotify Developer Dashboard.
4. Train model: `python train_model.py`
5. Run server: `python app.py`

### Frontend
1. Go to `frontend/`
2. Install packages: `npm install`
3. Run dev server: `npm run dev`
