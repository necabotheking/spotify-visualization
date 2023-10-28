import pandas as pd
import requests

from spotify_tableau_project.data_handling.spotify_streaming import main
from spotify_tableau_project.utils.constants import AUTH_URL, BASE_URL
from spotify_tableau_project.utils.functions import load_environment_variables


def get_access_token():
    """
    Gets the access token from the Spotify Accounts

    Inputs: None

    Returns:
        access_token (str): access token for the Spotify Web API
    """
    CLIENT_ID, CLIENT_SECRET = load_environment_variables()

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


def get_request():
    """
    Makes a post request and returns the access token to be included in the headers

    Inputs: None

    Returns: headers (str): HTTP headers
    """
    access_token = get_access_token()

    headers = {"Authorization": f"Bearer {access_token}"}

    return headers


def make_request(headers, track_uri):
    """
    Makes the get request to the Spotify Web API

    Inputs:
        headers (str): HTTP headers
        URI (str): the resource identifier of a spotify track

    Returns: r (dict): dictionary containing the request response data
    """
    # for testing
    print(f"Beginning Request for {track_uri}")

    r = requests.get(BASE_URL + "artists/" + track_uri, headers=headers)

    r = r.json()

    print(f"Request completed {track_uri}")

    return r


def make_artist_request(headers, artist_uri):
    """
    Makes a request for the artist and pulls the genres associated with that artist

    Inputs:
            headers (str): HTTP headers
            artist_uri (str): the resource identifier of an artist

    Returns: genre_lst (lst): list of genres associated with artist
    """
    artist_request = requests.get(BASE_URL + "artists/" + artist_uri, headers=headers)

    artist_request = artist_request.json()

    genre_lst = artist_request["genres"]

    return genre_lst


def pull_song_genre(streaming_dataframe):
    """
    Will utilize the get_request() function to make get requests for each song
    to get the genres associated and return the genres in a dataframe with the
    artists name

    Inputs: streaming_dataframe (Pandas DataFrame):

    Returns: expanded_genres_df (Pandas DataFrame): expanded DataFrame of genres from the developers spotify data
    """
    genre_dict = {}

    headers = get_request()
    # make POST and get access_token, headers for the GET calls

    # create a list of song URIs then call spotify web api
    uri_lst = streaming_dataframe["track_uri_clean"].to_list()

    for uri in uri_lst:
        track_info = make_request(headers, uri)

        artist_uri, artist_name = pull_artist_uri(track_info)

        genre_lst = make_artist_request(headers, artist_uri)

        genre_dict[artist_name] = genre_lst

    expanded_genres_df = dict_formatted_df(genre_dict)

    return expanded_genres_df


def dict_formatted_df(genre_dict):
    """
    Formats and expands the genre dataframe

    Inputs: genre_dict (Pandas DataFrame)

    Returns: expanded_df (Pandas DataFrame):
    """
    genre_df = pd.Series(genre_dict).to_frame("grenes")

    genre_df.reset_index(inplace=True, names="artist_name")

    expanded_df = genre_df.explode("genres")

    return expanded_df


def pull_artist_uri(track_information):
    """
    Pulls the artist uri and name

    Inputs:
            track_information (dict):

    Returns:
            artist_uri (str):
            artist_name (str):
    """
    artist_uri = track_information["artists"][0]["uri"].split(":")[2]

    artist_name = track_information["artists"][0]["name"]

    return artist_uri, artist_name


def main():
    """
    Runs the main program
    """
    _, all_year_streaming_df = main()
    pull_song_genre(all_year_streaming_df)
