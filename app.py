from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

# Initialize Flask app
app = Flask(__name__)

# Define correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
MODEL_PATH = os.path.join(BASE_DIR, "../models/trained_disease_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "../models/disease_label_encoder.pkl")
DATA_PATH = os.path.join(BASE_DIR, "../models/dataset.csv")
DESC_PATH = os.path.join(BASE_DIR, "../models/description.csv")
PRECAUTION_PATH = os.path.join(BASE_DIR, "../models/precaution.csv")

# Load trained model and label encoder
model = pickle.load(open(MODEL_PATH, "rb"))
label_encoder = pickle.load(open(ENCODER_PATH, "rb"))

# Load datasets
dataset = pd.read_csv(DATA_PATH)
description = pd.read_csv(DESC_PATH)
precautions = pd.read_csv(PRECAUTION_PATH)

# Extract symptom columns from dataset
symptom_columns = dataset.columns[1:].tolist()  # Exclude "Disease" column


def predict_disease(symptoms):
    """
    Predict the disease based on user-provided symptoms.
    """
    # Convert symptoms to lowercase
    symptoms = [symptom.lower().strip() for symptom in symptoms]
    
    # Convert symptoms into a one-hot encoding vector
    input_vector = np.zeros(len(symptom_columns))

    for symptom in symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.index(symptom)
            input_vector[index] = 1  # Mark symptom as present
    
    # Predict disease
    prediction = model.predict([input_vector])[0]
    predicted_disease = label_encoder.inverse_transform([prediction])[0]
    return predicted_disease


def get_description(disease):
    """
    Retrieve the description of a given disease.
    """
    desc_row = description[description["Disease"] == disease]
    return desc_row["Description"].values[0] if not desc_row.empty else "No description available."


def get_precautions(disease):
    """
    Retrieve the precautions for a given disease.
    """
    prec_row = precautions[precautions["Disease"] == disease]
    if not prec_row.empty:
        return prec_row.iloc[0, 1:].dropna().tolist()  # Get non-null precaution values
    return ["No specific precautions available."]


@app.route("/")
def home():
    """
    Render the main chatbot interface.
    """
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    API endpoint to predict a disease based on symptoms.
    """
    data = request.json
    symptoms = data.get("symptoms", [])

    if not symptoms:
        return jsonify({"error": "No symptoms provided."}), 400
    
    predicted_disease = predict_disease(symptoms)
    response = {"disease": predicted_disease}
    return jsonify(response)


@app.route("/description", methods=["POST"])
def disease_description():
    """
    API endpoint to retrieve the description of a disease.
    """
    data = request.json
    disease = data.get("disease", "")

    if not disease:
        return jsonify({"error": "No disease provided."}), 400

    desc = get_description(disease)
    return jsonify({"description": desc})


@app.route("/precautions", methods=["POST"])
def disease_precautions():
    """
    API endpoint to retrieve precautions for a disease.
    """
    data = request.json
    disease = data.get("disease", "")

    if not disease:
        return jsonify({"error": "No disease provided."}), 400

    prec = get_precautions(disease)
    return jsonify({"precautions": prec})


if __name__ == "__main__":
    app.run(debug=True)
