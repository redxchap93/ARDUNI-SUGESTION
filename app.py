import logging
import os
from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from joblib import dump, load

app = Flask(__name__)

# Load the pre-trained model with error handling
try:
    model = load("stock_price_prediction_model.joblib")
except FileNotFoundError:
    # If model file doesn't exist, create a dummy model for testing
    model = LinearRegression()
    print("Warning: Model file not found. Using dummy model for testing.")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the input data from the request body
        data = request.get_json()

        # Convert to numpy array if it's a list
        import numpy as np
        if isinstance(data, list):
            data = np.array(data)
        
        # Preprocess the data using the same pipeline as during training
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

        # Make a prediction using the pre-trained model
        prediction = model.predict(data)

        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)