# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import joblib
# import pandas as pd
# import os

# # Load trained model
# model = joblib.load("model.pkl")

# # Initialize Flask app
# app = Flask(__name__)  # ✅ Corrected

# # Enable CORS
# CORS(app, origins="*", supports_credentials=True)  # ✅ Allow all origins

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST', 'OPTIONS'])
# def predict():
#     if request.method == "OPTIONS":
#         return '', 204  # ✅ Handle preflight request

#     try:
#         data = request.get_json()  # ✅ Get JSON data

#         state = data['state']
#         district = data['district']
#         season = data['season']
#         crop = data['crop']
#         area = float(data['area'])

#         # Create input DataFrame
#         user_input = pd.DataFrame([[state, district, season, crop, area]],
#                                   columns=['State_Name', 'District_Name', 'Season', 'Crop', 'Area'])

#         # Predict production
#         prediction = model.predict(user_input)[0]

#         return jsonify({'prediction': round(float(prediction), 2)})  # ✅ Return JSON response

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500  # ✅ Handle errors

# # Run Flask app
# if __name__ == '__main__':  # ✅ Corrected
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

# Load trained model
model = joblib.load("model.pkl")

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all origins (adjust as needed)
CORS(app, resources={r"/predict": {"origins": "*"}}, supports_credentials=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'OPTIONS'])  # Handle OPTIONS for preflight
def predict():
    if request.method == "OPTIONS":
        return '', 204  # Return HTTP 204 No Content for preflight requests

    try:
        # Ensure JSON request
        if not request.is_json:
            return jsonify({'error': "Request must be JSON"}), 415

        # Parse JSON data
        data = request.get_json()

        # Extract fields with validation
        state = data.get("state")
        district = data.get("district")
        season = data.get("season")
        crop = data.get("crop")
        area = data.get("area")

        if not all([state, district, season, crop, area]):
            return jsonify({'error': "Missing required fields"}), 400

        # Convert area to float safely
        try:
            area = float(area)
        except ValueError:
            return jsonify({'error': "Invalid area value"}), 400

        # Create input DataFrame
        user_input = pd.DataFrame([[state, district, season, crop, area]],
                                  columns=['State_Name', 'District_Name', 'Season', 'Crop', 'Area'])

        # Predict production
        prediction = model.predict(user_input)[0]

        return jsonify({'prediction': round(float(prediction), 2)})  # Return JSON response

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error details


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

