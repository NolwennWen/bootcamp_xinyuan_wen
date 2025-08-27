from flask import Flask, request, jsonify
import threading
import matplotlib.pyplot as plt
import io
import base64
import pickle
import numpy as np

app = Flask(__name__)

# ===== Load the trained model =====
import os
import pickle

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # if run as script
except NameError:
    BASE_DIR = os.getcwd()  # if run in notebook

MODEL_PATH = os.path.join(BASE_DIR, "model", "final_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ===== Routes =====

@app.route('/predict', methods=['POST'])
def predict():
    """
    POST /predict
    Expects JSON input: {"features": [f1, f2, ..., fn]}
    Returns model prediction as JSON.
    """
    data = request.get_json()
    features = data.get('features', None)
    if features is None:
        return jsonify({'error': 'No features provided'}), 400
    try:
        X = np.array(features).reshape(1, -1)
        pred = model.predict(X)
        return jsonify({'prediction': float(pred[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict/<float:input1>', methods=['GET'])
def predict_one(input1):
    """
    GET /predict/<input1>
    Accepts a single feature value. 
    All other features are filled with 0.
    """
    try:
        X = np.array([[input1] + [0]*(len(model.coef_)-1)])
        pred = model.predict(X)
        return jsonify({'prediction': float(pred[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict/<float:input1>/<float:input2>', methods=['GET'])
def predict_two(input1, input2):
    """
    GET /predict/<input1>/<input2>
    Accepts two feature values.
    All other features are filled with 0.
    """
    try:
        X = np.array([[input1, input2] + [0]*(len(model.coef_)-2)])
        pred = model.predict(X)
        return jsonify({'prediction': float(pred[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/plot')
def plot():
    """
    GET /plot
    Returns a simple example chart as an inline image.
    """
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4], marker="o", color="orange")
    ax.set_title("Sample Plot")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_bytes = base64.b64encode(buf.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{img_bytes}"/>'


def run_flask():
    app.run(port=5000, debug=True)

# Start Flask in a separate thread (useful inside Jupyter Notebook).
# If running from terminal, just use: python app.py
threading.Thread(target=run_flask).start()
