from flask.testing import FlaskClient
import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_webhook(client: FlaskClient):
    """Test the /webhook endpoint with a sample message."""
    response = client.post('/webhook', json={"message": "Tell me about data types"})
    json_data = response.get_json()
    assert response.status_code == 200
    assert "This is a placeholder response for the message" in json_data['message']
