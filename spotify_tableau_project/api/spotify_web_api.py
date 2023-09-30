import os
import json
from dotenv import load_dotenv
import requests
from spotify_tableau_project.data_handling.spotify_streaming import main

BASE_URL = "https://api.spotify.com/v1/"
# set URL to artists and track info
REDIRECT_URL = "http://localhost:8888/callback"


def load_environment_variables():
    """
    Loads the environment variables and sets the AUTH_URL

    Inputs: None

    Returns: CLIENT_ID (str)
            CLIENT_SECRET (str)
            AUTH_URL (str)
    """
    load_dotenv("spotify_tableau_project/credentials/.env")

    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    AUTH_URL = "https://accounts.spotify.com/api/token"

    return CLIENT_ID, CLIENT_SECRET, AUTH_URL


def get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL):
    """
    Gets the access token from the Spotify Accounts

    Inputs:
        CLIENT_ID: (str)
        CLIENT_SECRET: (str)
        AUTH_URL: (str)

    Returns: access_token (str)
    """
    CLIENT_ID, CLIENT_SECRET, AUTH_URL = load_environment_variables()

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
        BASE_URL: (str)

    Returns: requst
    """
    #access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL)

    headers = {"Authorization": f"Bearer {access_token}"}

    # r = requests.get(BASE_URL + url_to_add, headers=headers)

    return headers

def make_request(access_token, headers, BASE_URL, URI):
    """
    Makes the get request to the Spotify Web API
    
    Inputs:
        access_token:
        headers:
        BASE_URL
        URI:
    
    Returns:
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    r = requests.get(BASE_URL + 'tracks/' + URI, headers=headers)
    
    r = r.json()
    # grab the genres associated with the artist of this song
    return 

def pull_song_genre(CLIENT_ID, CLIENT_SECRET, AUTH_URL, BASE_URL):
    """
    Will utilize the get_request() function to make get requests for each song
    to get the genres associated

    Inputs: None

    Returns: (Pandas DataFrame)
    """
    _ , all_year_streaming_df = main()
    #access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTH_URL)
    #headers = get_request()
    
    # check for song genre
    uri_lst = all_year_streaming_df['track_uri_clean'].to_list()
    
    for indx, uri in enumerate(uri_lst):
        request = get_request
        # make the requst then add the 
        
        # makes multiple requests for the token. Need to make one request
        # THEN multiple get requests

def pull_episode_genre():
    """
    
    """
    pass


def merge_genre_dataframe():
    """
    
    """
    pass


def main():
    """
    Runs the main program
    """
    pull_song_genre()
    # should generate the dataframes, make a post and get request,
    # then iterate through the data frames to add the genres making requests.
