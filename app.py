from flask import Flask, request, render_template
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(__name__, template_folder='templates')

model_and_vectorizer = pickle.load(open('C:/Users/user/Pictures/ITC/ITCI5_(2024-2025)/Artificial Intelligence/Project/Final_Project/models/model_and_vectorizer.pkl', 'rb'))

print(model_and_vectorizer)

model = model_and_vectorizer.get('model')
vectorizer = model_and_vectorizer.get('vectorizer')

if model is None or vectorizer is None:
    print("Model or vectorizer not found in the pickle file.")
    exit(1) 
categories = ['business', 'entertainment', 'politics', 'sport', 'tech']

def preprocess_text(text):
    text_vectorized = vectorizer.transform([text])
    return text_vectorized

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        document = request.form['document']
        
        if not document.strip():  
            return render_template('index.html', message="Please enter a document.")

        processed_input = preprocess_text(document)
        
        predicted_probs = model.predict(processed_input)
        predicted_class = np.argmax(predicted_probs)
        predicted_category = categories[predicted_class]
        
        return render_template('result.html', prediction=predicted_category)

# To run Flask app
if __name__ == "__main__":
    app.run(debug=True)
