import os
import json
from dotenv import load_dotenv
import requests


load_dotenv("spotify_tableau_project/credentials/.env")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

BASE_URL = "https://api.spotify.com/v1/"
# set URL to artists and track info
AUTH_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URL = "http://localhost:8888/callback"


def get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL):
    """
    Gets the access token from the Spotify Accounts

    Inputs:
        CLIENT_ID: (str)
        CLIENT_SECRET: (str)
        AUTH_URL: (str)

    Returns: access_token (str)
    """
    # POST
    auth_response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    # convert response to JSON
    auth_response_data = auth_response.json()

    # save and return the access token
    access_token = auth_response_data["access_token"]

    return access_token


def get_request(CLIENT_ID, CLIENT_SECRET, AUTH_URL, BASE_URL):
    """
    Describe function here

    Inputs:
        CLIENT_ID: (str)
        CLIENT_SECRET: (str)
        AUTH_URL: (str)
        URL: (str)

    Returns: requst
    """
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL)

    headers = {"Authorization": f"Bearer {access_token}"}

    # r = requests.get(BASE_URL + url_to_add, headers=headers)

    return headers
