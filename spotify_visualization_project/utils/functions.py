"""
Constant functions to be used within the program
"""

import os

from dotenv import load_dotenv


def load_environment_variables():
    """
    Loads the environment variables and sets the AUTH_URL

    Inputs: None

    Returns:
            CLIENT_ID (str): client credentials for spotify web api
            CLIENT_SECRET (str): client credentials for spotify web api
    """
    load_dotenv("spotify_visualization_project/credentials/.env")

    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    return CLIENT_ID, CLIENT_SECRET