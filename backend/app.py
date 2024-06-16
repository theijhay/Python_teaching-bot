from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
import logging
from flask_cors import CORS
from celery import Celery
from flask_limiter import Limiter
from dotenv import load_dotenv
import os
from my_celery import Celery
from models import Base, UserProgress, session
from logging_config import setup_logging
from flask import request
from rasa_utils import load_specific_model
import asyncio


# Initialize Flask app
app = Flask(__name__)
CORS(app)


# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('App startup')

# Load environment variables from .env file
load_dotenv()

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['broker_connection_retry_on_startup'] = True


# Create Celery instance
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Setup the logging
setup_logging()


# Specify model name
model_name = '20240608-130304-claret-squircle.tar.gz'

# Load the Rasa model
try:
    nlu_agent = load_specific_model(model_name)
except FileNotFoundError as e:
    logging.error(e)
    nlu_agent = None


# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return "Welcome to the Python Teaching Bot!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive messages from users.
    
    Returns:
    - json: The status of the message processing.
    """
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({"status": "failed", "reason": "No message provided"}), 400
    
    task = handle_user_message.apply_async(args=[message])
    return jsonify({"status": "processing", "task_id": task.id})

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("App startup")

# Define the Celery task
@celery.task
def handle_user_message(message):
    # Log the received message
    logger.info(f"Received message: {message}")
    
    # Define an asynchronous function to process the message
    async def process_message(message):
        # Call the NLU agent to parse the message and generate a response
        response = await nlu_agent.parse_message(message)
        response_text = response['text']
        # Log the generated response
        logger.info(f"Generated response: {response_text}")

        # Simulate a database operation to save user progress
        user_progress = UserProgress(user_id=1, progress_info=response_text)
        session.add(user_progress)
        session.commit()
        # Log the successful saving of user progress to the database
        logger.info("User progress saved to the database.")
        return response_text
    
    # Get the current event loop or create a new one
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Run the asynchronous process_message function until it completes
    response_text = loop.run_until_complete(process_message(message))
    return response_text

if __name__ == '__main__':
    app.run(debug=True, port=5000)
