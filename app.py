from flask import Flask, request, jsonify, render_template
from collections import defaultdict
from datetime import datetime
import json
import joblib
import pandas as pd
import random
import threading
import time

app = Flask(__name__)

# Load models for individual prediction
models = {
    'Logistic Regression': joblib.load('Logistic_Regression.pkl'),
    'Neural Network': joblib.load('Neural_Network.pkl'),
    'Naive Bayes': joblib.load('Naive_Bayes.pkl'),
    'Decision Tree': joblib.load('Decision_Tree.pkl'),
    'Random Forest': joblib.load('Random_Forest.pkl')
}
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Data storage for logs (for dashboard visualization)
logs = []
last_prediction = {}
model_counts = defaultdict(lambda: {'intrusion': 10, 'no_intrusion': 10})  # Initial balanced counts for simplicity

# Route to display the prediction template
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle individual predictions (for /predict)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data['features']
        
        # Process and scale features
        feature_names = ['Source Port', 'Destination Port', 'Protocol', 'Packet Length', 'TTL', 'Flags', 
                         'Flow Duration', 'Packet Count', 'Average Packet Size', 'Payload Size', 'Window Size', 'Urgent Pointer']
        sample_df = pd.DataFrame([features], columns=feature_names)

        for column, le in label_encoders.items():
            sample_df[column] = sample_df[column].apply(lambda x: le.transform(['Unknown'])[0] if x not in le.classes_ else le.transform([x])[0])

        X_scaled = scaler.transform(sample_df)

        # Run predictions with each model
        results = {}
        for name, model in models.items():
            results[name] = int(model.predict(X_scaled)[0])

        # Update last_prediction for viewing the most recent result
        timestamp = datetime.now().isoformat()
        last_prediction.update({'timestamp': timestamp, 'features': features, 'results': results})

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to handle real-time packet logs for the dashboard
@app.route('/log_prediction', methods=['POST'])
def log_prediction():
    try:
        data = request.get_json()
        timestamp = datetime.now().isoformat()
        logs.append({ 'timestamp': timestamp, 'models': data['models'], 'packet_details': data['packet_details'] })

        return jsonify({"status": "success", "message": "Log captured"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Route to clear logs for a fresh start
@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    logs.clear()
    for model in model_counts:
        model_counts[model] = {'intrusion': 10, 'no_intrusion': 10}  # Reset counts for simplicity
    return jsonify({"status": "success", "message": "Logs cleared"}), 200

# Route to serve the dashboard
@app.route('/dashboard')
def dashboard():
    chart_data = {
        'labels': list(model_counts.keys()),
        'intrusion_counts': [model_counts[model]['intrusion'] for model in model_counts],
        'no_intrusion_counts': [model_counts[model]['no_intrusion'] for model in model_counts]
    }

    return render_template('dashboard.html', chart_data=json.dumps(chart_data), last_prediction=last_prediction)

# Endpoint for fetching real-time logs for dashboard
@app.route('/logs')
def get_logs():
    return jsonify(logs)

# Endpoint for getting the latest prediction for the dashboard
@app.route('/last_prediction')
def last_prediction_route():
    return jsonify(last_prediction)

# Balanced simulation of intrusion logs
def simulate_balanced_intrusion_task():
    while True:
        selected_model = random.choice(list(models.keys()))

        # Check if we can add an intrusion and balance counts accordingly
        if model_counts[selected_model]['no_intrusion'] > 0:
            # Add an intrusion and reduce no intrusion count
            model_counts[selected_model]['intrusion'] += 1
            model_counts[selected_model]['no_intrusion'] -= 1

            # Log entry for simulated intrusion
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "models": {
                    selected_model: {
                        "prediction": 1,
                        "intrusion_status": "Intrusion Detected"
                    }
                },
                "packet_details": {
                    'Source Port': random.randint(1024, 65535),
                    'Destination Port': random.randint(1024, 65535),
                    'Protocol': random.choice([1, 6, 17]),
                    'Packet Length': random.randint(40, 1500),
                    'TTL': random.randint(1, 128),
                    'Flags': random.choice([0, 1]),
                    'Flow Duration': random.randint(1, 1000),
                    'Packet Count': random.randint(1, 10),
                    'Average Packet Size': random.randint(40, 1500),
                    'Payload Size': random.randint(0, 1400),
                    'Window Size': random.randint(1, 65535),
                    'Urgent Pointer': random.randint(0, 1)
                }
            }
            logs.append(log_entry)

        # Sleep before the next update
        time.sleep(30)

# Start balanced intrusion simulation task
intrusion_simulation_thread = threading.Thread(target=simulate_balanced_intrusion_task)
intrusion_simulation_thread.daemon = True
intrusion_simulation_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
