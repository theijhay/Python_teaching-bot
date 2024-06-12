import os
from rasa.core.agent import Agent

def load_specific_model(model_name):
    """
    Load a specific Rasa model given the model name.

    Args:
    - model_name (str): The name of the model file.

    Returns:
    - Agent: An agent object that can be used to parse messages.
    """
    model_path = os.path.join('models', model_name)
    if os.path.exists(model_path):
        agent = Agent.load(model_path)
        return agent
    else:
        raise FileNotFoundError(f"Model {model_name} not found in the models directory.")
