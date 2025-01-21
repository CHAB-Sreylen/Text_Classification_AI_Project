from flask import Flask, request, render_template
import nltk
import pickle
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

app = Flask(__name__, template_folder='templates')

MODEL_PATH = './models'
MODEL_NAME = {
    "LSTM": "LSTM_model.keras",
    "GRU": "GRU_model.keras",
    "ANN": "ANN_model.pkl",
}
RESULT = {
    "business": "Business",
    "entertainment": "Entertainment",
    "politics": "Politics",
    "sport": "Sport",
    "tech": "Technology",
}

categories = ['business', 'entertainment', 'politics', 'sport', 'tech']

def preprocess_text_ANN(text, vectorizer):
    text_vectorized = vectorizer.transform([text])
    return text_vectorized

def preprocess_text_KERAS(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    processed_text = ' '.join(tokens)
    return processed_text

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        document = request.form.get('document', '').strip()
        uploaded_file = request.files.get('file')
        selected_model = request.form['model']

        # Check if text or file is provided
        if not document and not uploaded_file:
            return render_template('index.html', message="Please enter a document or upload a file.")

        # Process the uploaded file if provided
        if uploaded_file and uploaded_file.filename.endswith('.txt'):
            document = uploaded_file.read().decode('utf-8').strip()

        if not document:
            return render_template('index.html', message="The uploaded file is empty or invalid.")

        # Handle model-specific preprocessing and prediction
        if selected_model == 'ANN':
            model_and_vectorizer = pickle.load(open(f'{MODEL_PATH}/{MODEL_NAME[selected_model]}', 'rb'))
            model = model_and_vectorizer.get('model')
            vectorizer = model_and_vectorizer.get('vectorizer')

            if model is None or vectorizer is None:
                return render_template('index.html', message="Error loading ANN model or vectorizer.")

            processed_input = preprocess_text_ANN(document, vectorizer)
            predicted_probs = model.predict(processed_input)
            predicted_class = np.argmax(predicted_probs)
            predicted_category = categories[predicted_class]

        elif selected_model in ['LSTM', 'GRU']:
            model = load_model(f'{MODEL_PATH}/{MODEL_NAME[selected_model]}')

            with open(f'{MODEL_PATH}/tokenizer.json', 'r') as f:
                tokenizer_json = f.read()
                tokenizer = tokenizer_from_json(tokenizer_json)

            processed_text = preprocess_text_KERAS(document)
            sequences = tokenizer.texts_to_sequences([processed_text])
            padded = pad_sequences(sequences, maxlen=200)

            prediction = model.predict(padded)
            predicted_category = categories[prediction.argmax()]

        else:
            return render_template('index.html', message="Invalid model selection.")

        return render_template('result.html', prediction=RESULT[predicted_category])


# To run Flask app
if __name__ == "__main__":
    app.run(debug=True)
