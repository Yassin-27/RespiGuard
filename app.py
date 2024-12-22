import os
import librosa
import numpy as np
import requests
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load the trained model (make sure to train your model and save it, or implement the training in this script)
# For demonstration, we will create a simple model here.

# Function to extract features from audio files
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=5.0)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to load dataset and prepare data (for training)
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

# Load your data and train the model here if needed
data_directory = '/path/to/your/data'  # Update this path
X, y = load_data(data_directory)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

@app.route('/analyze_sound', methods=['POST'])
def analyze_sound():
    audio_file = request.files['file']
    audio_path = 'temp.wav'
    audio_file.save(audio_path)  # Save the uploaded file temporarily
    mfccs = extract_features(audio_path)
    if mfccs is not None:
        mfccs = mfccs.reshape(1, -1)
        prediction = model.predict(mfccs)
        os.remove(audio_path)  # Clean up the temporary file
        return jsonify({'diagnosis': prediction[0]})
    else:
        return jsonify({'error': 'Failed to analyze sound'}), 400

# Get environmental data from OpenWeatherMap
@app.route('/get_environmental_data', methods=['GET'])
def get_environmental_data():
    api_key = '3998e2e5095ecacf4ee5d0be174f951c'  # Replace with your API key
    city = 'Cairo,eg'
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to retrieve environmental data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
