from celery import Celery

def make_celery(app):
    """
    Create a Celery object and configure it with the Flask app's settings.

    Parameters:
    - app: The Flask application instance.

    Returns:
    - A configured Celery object.
    """
    # Create a Celery object with the name of the Flask app
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']  # Set the broker URL from the app's config
    )
    # Update Celery's configuration with the Flask app's configuration
    celery.conf.update(app.config)
    return celery  # Return the configured Celery object

