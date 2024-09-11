from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd

# Initialize Flask application
app = Flask(__name__)

# Load the trained models
models = {
    'Logistic Regression': joblib.load('Logistic_Regression.pkl'),
    'Neural Network': joblib.load('Neural_Network.pkl'),
    'Naive Bayes': joblib.load('Naive_Bayes.pkl'),
    'Decision Tree': joblib.load('Decision_Tree.pkl'),
    'Random Forest': joblib.load('Random_Forest.pkl')
}

# Load the scaler and encoders
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Serve the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the request
        data = request.get_json()
        features = data['features']
        
        # Create a DataFrame from the input features
        feature_names = [
            'Source Port', 'Destination Port', 'Protocol', 'Packet Length', 
            'TTL', 'Flags', 'Flow Duration', 'Packet Count', 
            'Average Packet Size', 'Payload Size', 'Window Size', 'Urgent Pointer'
        ]
        new_sample_df = pd.DataFrame([features], columns=feature_names)
        
        # Encode categorical variables using the saved label encoders
        for column, le in label_encoders.items():
            new_sample_df[column] = le.transform(new_sample_df[column])
        
        # Scale the new sample data using the loaded scaler
        X_new_sample = scaler.transform(new_sample_df)
        
        # Store results for all models
        results = {}

        # Predict with each model
        for name, model in models.items():
            prediction = model.predict(X_new_sample)
            results[name] = int(prediction[0])  # Convert prediction to integer

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
