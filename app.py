from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

# Load trained model
model = joblib.load("model.pkl")

# Initialize Flask app
app = Flask(_name_)  # ✅ Corrected

# Enable CORS
CORS(app, origins="*", supports_credentials=True)  # ✅ Allow all origins

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == "OPTIONS":
        return '', 204  # ✅ Handle preflight request

    try:
        data = request.get_json()  # ✅ Get JSON data

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

        return jsonify({'prediction': round(float(prediction), 2)})  # ✅ Return JSON response

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # ✅ Handle errors

# Run Flask app
if _name_ == '_main_':  # ✅ Corrected
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
