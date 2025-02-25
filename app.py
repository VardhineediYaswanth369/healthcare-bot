from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Initialize Flask app
app = Flask(__name__)

# Load trained model and label encoder
MODEL_PATH = "app/model/trained_disease_model.pkl"
ENCODER_PATH = "app/model/disease_label_encoder.pkl"
DATA_PATH = "app/model/dataset.csv"
DESC_PATH = "app/model/description.csv"
PRECAUTION_PATH = "app/model/precaution.csv"

model = pickle.load(open(MODEL_PATH, "rb"))
label_encoder = pickle.load(open(ENCODER_PATH, "rb"))

dataset = pd.read_csv(DATA_PATH)
description = pd.read_csv(DESC_PATH)
precautions = pd.read_csv(PRECAUTION_PATH)

def predict_disease(symptoms):
    # Convert symptoms into one-hot encoding
    input_vector = np.zeros(len(dataset.columns) - 1)
    for symptom in symptoms:
        if symptom in dataset.columns:
            input_vector[dataset.columns.get_loc(symptom) - 1] = 1
    
    # Predict disease
    prediction = model.predict([input_vector])[0]
    predicted_disease = label_encoder.inverse_transform([prediction])[0]
    return predicted_disease

def get_description(disease):
    desc_row = description[description["Disease"] == disease]
    return desc_row["Description"].values[0] if not desc_row.empty else "No description available."

def get_precautions(disease):
    prec_row = precautions[precautions["Disease"] == disease]
    if not prec_row.empty:
        return prec_row.iloc[0, 1:].dropna().tolist()
    return ["No specific precautions available."]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    symptoms = data.get("symptoms", [])
    
    if not symptoms:
        return jsonify({"error": "No symptoms provided."})
    
    predicted_disease = predict_disease(symptoms)
    response = {"disease": predicted_disease}
    return jsonify(response)

@app.route("/description", methods=["POST"])
def disease_description():
    data = request.json
    disease = data.get("disease", "")
    
    if not disease:
        return jsonify({"error": "No disease provided."})
    
    desc = get_description(disease)
    return jsonify({"description": desc})

@app.route("/precautions", methods=["POST"])
def disease_precautions():
    data = request.json
    disease = data.get("disease", "")
    
    if not disease:
        return jsonify({"error": "No disease provided."})
    
    prec = get_precautions(disease)
    return jsonify({"precautions": prec})

if __name__ == "__main__":
    app.run(debug=True)
