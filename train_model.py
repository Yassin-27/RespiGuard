import os
import librosa
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Function to extract features from audio files
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=5.0)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to load dataset and prepare data
def load_data(data_dir):
    features = []
    labels = []

    for file in os.listdir(data_dir):
        if file.endswith('.wav'):
            label = file.split('_')[0]
            if label == "asthma":
                label = "wheeze"
            file_path = os.path.join(data_dir, file)
            mfccs = extract_features(file_path)
            if mfccs is not None:
                features.append(mfccs)
                labels.append(label)

    return np.array(features), np.array(labels)

# Load data
data_directory = '/Users/yassinali/Downloads/RespiGuard website/data'  # تأكد من أن هذا هو المسار الصحيح
X, y = load_data(data_directory)

# Split data into training and testing sets
if len(X) > 0 and len(y) > 0:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'model.pkl')  # لحفظ النموذج في ملف

    # Predict on test data
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Model Accuracy: {accuracy * 100:.2f}%')
else:
    print("No data available for training and testing. Please check the data directory.")
