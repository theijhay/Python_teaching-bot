from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserProgress
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Python Teaching Bot!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    response = handle_user_message(data['message'])
    return jsonify({"message": response})

def handle_user_message(message):
    # Placeholder function to process the message and generate a response.
    # Integrate with Rasa or handle simple message responses here.
    return "This is a placeholder response for the message: " + message

if __name__ == '__main__':
    app.run(debug=True, port=5000)