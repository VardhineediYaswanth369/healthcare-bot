from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load trained model and label encoder
MODEL_PATH = "model/trained_disease_model.pkl"
ENCODER_PATH = "model/disease_label_encoder.pkl"

model = pickle.load(open(MODEL_PATH, "rb"))
label_encoder = pickle.load(open(ENCODER_PATH, "rb"))

# Define symptoms manually (from training data)
SYMPTOMS_LIST = [
    "fever", "cough", "fatigue", "headache", "sore_throat", "shortness_of_breath",
    "body_pain", "nausea", "vomiting", "diarrhea", "loss_of_smell", "loss_of_taste"
]  # Add actual symptoms from training

def predict_disease(symptoms):
    """
    Predict the disease based on user symptoms.
    """
    symptoms = [s.lower().strip() for s in symptoms]  # Normalize input
    input_vector = np.zeros(len(SYMPTOMS_LIST))

    for symptom in symptoms:
        if symptom in SYMPTOMS_LIST:
            index = SYMPTOMS_LIST.index(symptom)
            input_vector[index] = 1  # Mark symptom as present
    
    # Predict disease
    prediction = model.predict([input_vector])[0]
    predicted_disease = label_encoder.inverse_transform([prediction])[0]
    return predicted_disease

@app.route("/")
def home():
    """
    Render the chatbot UI.
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    API endpoint to predict disease from symptoms.
    """
    data = request.json
    symptoms = data.get("symptoms", [])

    if not symptoms:
        return jsonify({"error": "No symptoms provided."}), 400
    
    predicted_disease = predict_disease(symptoms)
    return jsonify({"disease": predicted_disease})

if __name__ == "__main__":
    app.run(debug=True)
