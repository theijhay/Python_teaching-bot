from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
import logging
from flask_limiter import Limiter
from dotenv import load_dotenv
import os
from my_celery import Celery
from models import Base, UserProgress, session
from logging_config import setup_logging
from flask import request
from rasa_utils import load_specific_model 

app = Flask(__name__)

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
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['RESULT_BACKEND'] = os.getenv('RESULT_BACKEND')
result_backend = 'redis://localhost:6379/0'
broker_connection_retry_on_startup = True

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=result_backend)
celery.conf.update(app.config)

# Set up logging
setup_logging()

# Load Rasa model
model_name = '20240608-130304-claret-squircle.tar.gz'  # This the rasa model name.
nlu_agent = load_specific_model(model_name)


# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return "Welcome to the Python Teaching Bot!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    response = handle_user_message.delay(data['message'])
    return jsonify({"status": "processing", "task_id": response.id})

@celery.task
def handle_user_message(message):
    logger.info(f"Received message: {message}")
   # The NLU agent to parse the message
    parsed_data = nlu_agent.interpreter.parse(message)
    response = f"This is a placeholder response. Parsed intent: {parsed_data['intent']['name']}"
    
    # Simulate database operation
    user_progress = UserProgress(user_id=1, progress_info=response)
    session.add(user_progress)
    session.commit()
    logger.info("User progress saved to the database.")
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
