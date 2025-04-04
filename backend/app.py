from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

print("Flask app is starting...")

# Load models during app startup to avoid loading them on each request
collab_model_path = os.path.join('models', 'collaborative_filtering_model.sav')
content_model_path = os.path.join('models', 'content_model.sav')

try:
    collab_model = joblib.load(collab_model_path)
    content_model = joblib.load(content_model_path)
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")

# Root endpoint to verify server status
@app.route('/')
def home():
    return jsonify({'message': 'Backend is running'})

# Collaborative filtering route
@app.route('/api/recommendations/collaborative', methods=['POST'])
def collaborative_recommendations():
    data = request.get_json()
    item_id = data.get('item_id')

    # Placeholder for collaborative filtering logic
    # Example response for now
    recommendations = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5']
    return jsonify({'recommendations': recommendations})

# Content-based filtering route
@app.route('/api/recommendations/content', methods=['POST'])
def content_recommendations():
    data = request.get_json()
    item_id = data.get('item_id')

    # Placeholder for content filtering logic
    recommendations = ['ItemA', 'ItemB', 'ItemC', 'ItemD', 'ItemE']
    return jsonify({'recommendations': recommendations})

# Azure ML predictions route
@app.route('/api/recommendations/azure', methods=['POST'])
def azure_recommendations():
    data = request.get_json()
    item_id = data.get('item_id')

    # Placeholder for Azure ML endpoint call
    recommendations = ['ItemX', 'ItemY', 'ItemZ', 'ItemW', 'ItemV']
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    print("Running Flask app...")
    app.run(port=5000, debug=True)

