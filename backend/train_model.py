import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train():
    # Get the directory where this file is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Load dataset
    data_path = os.path.join(BASE_DIR, '..', 'dataset', 'music_dataset.csv')
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)

    # Clean column names and values (strip whitespace)
    df.columns = df.columns.str.strip()
    df['mood'] = df['mood'].str.strip()
    
    # Features and target
    X = df[['danceability', 'energy', 'loudness', 'tempo', 'valence']]
    y = df['mood']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Define pipeline with scaling and classifier
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(random_state=42))
    ])

    # Hyperparameter tuning
    param_grid = {
        'rf__n_estimators': [50, 100, 200],
        'rf__max_depth': [None, 10, 20],
        'rf__min_samples_split': [2, 5],
        'rf__min_samples_leaf': [1, 2]
    }

    print("Starting hyperparameter tuning...")
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print(f"Best parameters: {grid_search.best_params_}")

    # Evaluate model
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    model_dir = os.path.join(BASE_DIR, 'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'mood_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"\nModel trained and saved successfully at {model_path}")

if __name__ == "__main__":
    train()
