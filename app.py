from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

# Load trained model
model = joblib.load("model.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    state = request.form['state']
    district = request.form['district']
    season = request.form['season']
    crop = request.form['crop']
    area = float(request.form['area'])

    # Create input DataFrame
    user_input = pd.DataFrame([[state, district, season, crop, area]],
                              columns=['State_Name', 'District_Name', 'Season', 'Crop', 'Area'])

    # Predict production
    prediction = model.predict(user_input)[0]

    return render_template('index.html', prediction=round(prediction, 2))

if __name__ == '__main__':
    app.run(debug=True)
