🏥 AI-Based Intelligent Healthcare Chatbot

This is an AI-powered chatbot that helps users identify diseases based on symptoms and provides precautions and descriptions for known diseases. Built with Flask, Google Colab for model training, and a frontend using HTML, CSS, and JavaScript, this chatbot enables users to interact and get relevant medical information.

📌 Features

✅ Symptom Checker – Predicts diseases based on user-input symptoms.

✅ Disease Description – Provides a simple explanation of diseases.

✅ Precautions – Suggests precautions to take for different diseases.

✅ Interactive UI – Built with HTML, CSS, and JavaScript for an easy-to-use experience.


🛠️ Technologies Used

    Frontend: HTML, CSS, JavaScript
    Backend: Flask (Python)
    Model Training: Google Colab (uses machine learning)
    Data Storage: CSV files containing symptoms, diseases, precautions, and descriptions

📂 Project Structure

    /healthcare-bot
    │── /static
    │   ├── styles.css       # CSS file for styling
    │   ├── script.js        # JavaScript file for frontend interactions
    │── /templates
    │   ├── index.html       # Main chatbot interface
    │── /models
    │   ├── trained_disease_model.pkl  # Trained machine learning model
    │   ├── disease_label_encoder.pkl  # Label encoder for disease names
    │── app.py               # Flask backend
    │── requirements.txt     # Dependencies for the project
    │── README.md            # Project documentation (this file)

🚀 Installation & Setup

1️⃣ Clone the Repository

    git clone https://github.com/your-username/healthcare-bot.git
    cd healthcare-bot

2️⃣ Install Dependencies
Create a virtual environment and install the required libraries:

    pip install -r requirements.txt

3️⃣ Run the Flask Server

    python app.py

The chatbot should be running at http://127.0.0.1:5000/.


🏋️‍♂️ Training the Model (Google Colab)

If you want to retrain the model, follow these steps:

1.Open Google Colab and mount Google Drive.

2.Run the provided Colab notebook to train the model.

3.Save the trained model in the /models folder.


📬 API Endpoints

    Method	Endpoint	Description
    POST	/chat	    Accepts user input and returns chatbot responses


🤝 Contribution

Feel free to fork the repository and submit pull requests.


📝 License

This project is open-source under the MIT License.
