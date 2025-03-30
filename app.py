from flask import Flask, request, jsonify
import joblib
import pandas as pd 
import os
from flask_cors import CORS  # Import Flask-CORS

# Load trained model
model = joblib.load("model.pkl")

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (Allow frontend from React on localhost)
CORS(app, resources={r"/*": {"origins": "https://localhost:5173"}})

@app.route('/')
def home():
    return jsonify({"message": "Yield Prediction API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.json  

        # Extract input values
        state = data['state']
        district = data['district']
        season = data['season']
        crop = data['crop']
        area = float(data['area'])

        # Create input DataFrame
        user_input = pd.DataFrame([[state, district, season, crop, area]],
                                  columns=['State_Name', 'District_Name', 'Season', 'Crop', 'Area'])

        # Predict production
        prediction = model.predict(user_input)[0]

        return jsonify({"predicted_yield": round(prediction, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
