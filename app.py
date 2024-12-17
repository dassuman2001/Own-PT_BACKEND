from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from fuzzywuzzy import process
import nltk
from nltk.stem import WordNetLemmatizer
import logging
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Initialize logging
logging.basicConfig(filename="chatbot_api.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Download NLTK resources (only needed once)
try:
    nltk.download("punkt")
    nltk.download("wordnet")
except Exception as e:
    logging.error(f"Failed to download NLTK resources: {e}")
    print("Error: Unable to download NLTK resources. Check your internet connection.")

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the dataset
dataset_file = "data/dataset.json"
try:
    with open(dataset_file, "r") as file:
        dataset = json.load(file)
        logging.info("Dataset loaded successfully.")
except FileNotFoundError:
    logging.error(f"Dataset not found at {dataset_file}.")
    raise FileNotFoundError(f"Error: {dataset_file} not found. Ensure the file exists in the correct directory.")
except json.JSONDecodeError as e:
    logging.error(f"Error decoding dataset JSON: {e}")
    raise ValueError(f"Error: The dataset file {dataset_file} is not properly formatted.")

# Create a dictionary of questions and answers
qa_pairs = {item["question"]: item["answer"] for item in dataset}

def preprocess_query(query):
    """
    Preprocesses the query by tokenizing and lemmatizing.
    """
    try:
        tokens = nltk.word_tokenize(query, language="english")  # Specify language
        lemmatized = [lemmatizer.lemmatize(token.lower()) for token in tokens]
        return " ".join(lemmatized)
    except Exception as e:
        logging.error(f"Error in preprocessing query: {e}")
        return query

def chatbot(query):
    """
    Matches user query with the closest question from the dataset
    and returns the corresponding answer.
    """
    query = preprocess_query(query)
    closest_question, score = process.extractOne(query, qa_pairs.keys())
    if score > 60:  # Adjust threshold as needed
        logging.info(f"Matched query '{query}' to '{closest_question}' with score {score}.")
        return qa_pairs[closest_question]
    else:
        logging.warning(f"No good match found for query: {query}")
        return "Sorry, I don't understand. Can you rephrase?"

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """
    API endpoint to handle chat queries.
    """
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request. 'message' is required."}), 400
        
        user_message = data["message"]
        logging.info(f"Received query: {user_message}")
        bot_response = chatbot(user_message)
        return jsonify({"response": bot_response})
    except Exception as e:
        logging.error(f"Error processing chat query: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(debug=True)
