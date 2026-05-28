# GEMINI.md

## Project Name

AI Music Mood Classifier

---

# Project Overview

AI Music Mood Classifier is a full-stack machine learning application that predicts the mood of songs based on audio features. The project uses a React + Vite frontend and a Python Flask backend. Predictions are generated using a trained machine learning model and stored inside a JSON database.

The project demonstrates:

- Frontend and backend communication
- REST API integration
- Machine learning deployment
- JSON-based storage
- Responsive UI design

---

# Main Objective

The goal of this project is to classify music into emotional categories such as:

- Happy
- Sad
- Energetic
- Calm
- Romantic
- Angry

using audio feature inputs provided by users.

---

# Technology Stack

| Category | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python + Flask |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Database | JSON |
| API Communication | Axios |
| Styling | CSS |

---

# Software Architecture

```text
Frontend (React + Vite)
        |
        | REST API
        v
Backend (Flask Server)
        |
        v
Machine Learning Model
        |
        v
JSON Database
```

---

# Folder Structure

```text
AI-Music-Mood-Classifier/
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── MoodForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── History.jsx
│   │   │   └── Footer.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   │
│   ├── data/
│   │   └── songs.json
│   │
│   ├── model/
│   │   └── mood_model.pkl
│   │
│   ├── utils/
│   │   └── helper.py
│   │
│   ├── app.py
│   ├── train_model.py
│   ├── requirements.txt
│   └── config.py
│
├── dataset/
│   └── music_dataset.csv
│
├── docs/
│   └── architecture.md
│
├── README.md
├── GEMINI.md
└── .gitignore
```

---

# Frontend Details

## Frontend Responsibilities

- Take user input
- Send API requests
- Display predictions
- Show prediction history
- Render responsive UI

---

# Backend Details

## Backend Responsibilities

- Receive API requests
- Process input data
- Run ML predictions
- Store history in JSON
- Return prediction results

---

# Machine Learning Details

## ML Algorithm

Random Forest Classifier

---

# Input Features

| Feature | Description |
|---|---|
| Danceability | Dance suitability |
| Energy | Intensity level |
| Loudness | Audio loudness |
| Tempo | Song speed |
| Valence | Positivity score |

---

# API Endpoints

## Predict Mood

```http
POST /predict
```

### Request Example

```json
{
  "danceability": 0.85,
  "energy": 0.74,
  "loudness": -6,
  "tempo": 125,
  "valence": 0.91
}
```

### Response Example

```json
{
  "mood": "Happy",
  "confidence": "92%"
}
```

---

## Fetch Prediction History

```http
GET /history
```

---

# JSON Database Design

## songs.json

```json
[
  {
    "id": 1,
    "danceability": 0.85,
    "energy": 0.74,
    "tempo": 125,
    "mood": "Happy"
  }
]
```

---

# Frontend UI Idea

## Theme

Modern dark-themed music dashboard.

## UI Sections

### Navbar
Contains:
- Project name
- Navigation links

### Mood Input Form
Allows users to enter:
- Danceability
- Energy
- Loudness
- Tempo
- Valence

### Result Card
Displays:
- Predicted mood
- Confidence score

### History Panel
Shows:
- Previous predictions
- Stored JSON data

---

# Installation Steps

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-music-mood-classifier.git
```

---

# Backend Setup

## Move to Backend Folder

```bash
cd backend
```

## Create Virtual Environment

```bash
python -m venv env
```

## Activate Environment

### Windows

```bash
env\Scripts\activate
```

### Linux/Mac

```bash
source env/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Flask Server

```bash
python app.py
```

Backend URL:

```text
http://127.0.0.1:5000
```

---

# Frontend Setup

## Move to Frontend Folder

```bash
cd frontend
```

## Install Packages

```bash
npm install
```

## Run Vite Development Server

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Python Dependencies

```text
Flask
Flask-CORS
pandas
numpy
scikit-learn
joblib
```

---

# Sample requirements.txt

```txt
Flask==3.0.0
Flask-CORS==4.0.0
pandas==2.2.0
numpy==1.26.0
scikit-learn==1.4.0
joblib==1.3.2
```

---

# Core Functionalities

- Music mood prediction
- JSON data storage
- REST API communication
- Prediction history tracking
- Responsive frontend

---

# Future Improvements

- Upload MP3 support
- Spotify API integration
- Deep learning model
- User authentication
- Cloud deployment
- Real-time audio analysis
- Recommendation engine

---

# Advantages

- Simple architecture
- Easy to understand
- Beginner-friendly AI project
- Lightweight database solution
- Scalable backend structure

---

# Limitations

- JSON database is not suitable for large-scale systems
- Manual feature entry required
- Limited mood classification categories

---

# Deployment Suggestions

| Service | Purpose |
|---|---|
| Vercel | Frontend Hosting |
| Render | Flask Backend Hosting |
| Railway | Full Stack Deployment |
| GitHub | Version Control |

---

# Learning Outcomes

By completing this project, developers will learn:

- React frontend development
- Flask backend development
- Machine learning integration
- API creation and testing
- JSON database management
- Full-stack project structure

---

# Conclusion

AI Music Mood Classifier is a beginner-to-intermediate level machine learning web application that combines artificial intelligence with modern frontend and backend technologies. The project provides practical experience in full-stack development and ML deployment using a clean and scalable architecture.