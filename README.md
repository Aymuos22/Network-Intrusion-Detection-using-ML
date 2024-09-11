### `README.md`

```markdown
# Intrusion Detection System

An Intrusion Detection System (IDS) built using machine learning models to classify network traffic data as either "Intrusion Detected" or "No Intrusion Detected". This project utilizes a Flask backend to serve predictions from various trained models and a Bootstrap-styled HTML frontend for user interaction.

## Features

- **Multiple Machine Learning Models:** Includes Logistic Regression, Neural Network, Naive Bayes, Decision Tree, and Random Forest models for intrusion detection.
- **Flask Backend:** Handles incoming data, processes it using pre-trained models, and returns prediction results.
- **Bootstrap Frontend:** Provides a user-friendly form for submitting network traffic data and displays the prediction results in a readable format.
- **REST API:** Accepts JSON-formatted data via POST requests for easy integration with other systems.

## Project Structure


intrusion-detection-system/
│
├── models/
│   ├── Logistic_Regression.pkl
│   ├── Neural_Network.pkl
│   ├── Naive_Bayes.pkl
│   ├── Decision_Tree.pkl
│   ├── Random_Forest.pkl
│   ├── scaler.pkl
│   └── label_encoders.pkl
│
├── templates/
│   └── index.html
│
├── app.py
└── README.md
```

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Aymuos22/intrusion-detection-system.git
   cd intrusion-detection-system
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Run the Flask Application:**
   ```bash
   python app.py
   ```

2. **Access the Application:**
   Open your web browser and go to `http://127.0.0.1:5000` to view the Intrusion Detection form.

3. **Submit Data:**
   - Fill out the form with relevant network traffic data.
   - Click the "Submit" button to get predictions from the models.
   - The results will be displayed in a user-friendly format below the form.

## API Endpoint

- **POST /predict**
  - **Description:** Accepts JSON input with network traffic features and returns predictions from all models.
  - **Input:** JSON object with a key `features` that is an array of values in the required order.
  - **Output:** JSON object with predictions from each model.

  **Example Request:**
  ```json
  {
      "features": [40550, 3945, "TCP", 255, 161, "SYN", 4328, 100, 405, 333, 32259, 0]
  }
  ```

  **Example Response:**
  ```json
  {
      "Logistic Regression": 1,
      "Neural Network": 0,
      "Naive Bayes": 1,
      "Decision Tree": 1,
      "Random Forest": 0
  }
  ```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

![image](https://github.com/user-attachments/assets/bfa6deb0-8a08-4b9d-806a-f484f6c26536)
