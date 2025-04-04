from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

print("Flask app is starting...")  # Debugging output

# Load models (comment these out for now to see if they are the issue)
# content_model = joblib.load('content_model.sav')
# collab_model = joblib.load('collab_model.sav')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data.get('user_input')
    
    # Dummy response for debugging
    return jsonify({'message': 'API is working!', 'user_input': user_input})

if __name__ == '__main__':
    print("Running Flask app...")  # Debugging output
    app.run(port=5000, debug=True)
