import pandas as pd
import requests

from spotify_visualization_project.data_handling.spotify_streaming import (
    run_data_handling,
)
from spotify_visualization_project.utils.constants import AUTH_URL, BASE_URL
from spotify_visualization_project.utils.functions import load_environment_variables


def get_access_token() -> str:
    """
    Gets the access token from the Spotify Accounts

    Inputs: None

    Returns: access_token: access token for the Spotify Web API
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

    if "access_token" in auth_response_data:
        access_token = auth_response_data["access_token"]
        return access_token
    else:
        print("Access token not found in response:", auth_response_data)


def get_request() -> str:
    """
    Makes a post request and returns the access token to be included in the headers

    Inputs: None

    Returns: headers: HTTP headers
    """
    access_token = get_access_token()

    headers = {"Authorization": f"Bearer {access_token}"}

    return headers


def make_track_request(headers: str, track_uri: str) -> dict:
    """
    Makes the get request to the Spotify Web API for track info given a track_uri

    Inputs:
        headers: HTTP headers
        track_uri: the resource identifier of a spotify track

    Returns: response: dictionary containing the request response data
    """
    # for testing
    print(f"Beginning Request for {track_uri}")

    response = requests.get(BASE_URL + "tracks/" + track_uri, headers=headers)

    response = response.json()

    print(response)

    # artist_uri = response['artists'][0]['uri'].split(':')[2]

    print(f"Request completed {track_uri}")

    return response


def make_artist_request(headers: str, artist_uri: str) -> list:
    """
    Makes a request for the artist and pulls the genres associated with that artist

    Inputs:
            headers: HTTP headers
            artist_uri: the resource identifier of an artist

    Returns: genre_lst: list of genres associated with artist
    """
    artist_request = requests.get(BASE_URL + "artists/" + artist_uri, headers=headers)

    artist_request = artist_request.json()

    genre_lst = artist_request["genres"]

    return genre_lst


def pull_song_genre(streaming_dataframe: pd.DataFrame, batch_size=50) -> pd.DataFrame:
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
    uri_lst = streaming_dataframe["spotify_uri_clean"].to_list()

    # TODO: Use Dask or another parallel programming tool to run the genre pulling in batches
    for uri in uri_lst:
        track_info = make_track_request(headers, uri)

        artist_uri, artist_name = pull_artist_uri(track_info)

        genre_lst = make_artist_request(headers, artist_uri)

        genre_dict[artist_name] = genre_lst

    expanded_genres_df = dictionary_to_dataframe(genre_dict)

    return expanded_genres_df


def dictionary_to_dataframe(genre_dict: dict) -> pd.DataFrame:
    """
    Formats and expands the genre dataframe

    Inputs:
        genre_dict: dictionary of genres associated with an artist

    Returns: expanded_df (Pandas DataFrame):
    """
    genre_df = pd.Series(genre_dict).to_frame("genres")

    genre_df.insert(0, "artist_name", genre_df.index)
    genre_df.reset_index(inplace=True, drop=True)

    expanded_df = genre_df.explode("genres")

    return expanded_df


def pull_artist_uri(track_information: dict) -> (str, str):
    """
    Pulls the artist uri and name

    Inputs:
            track_information: dictionary containing the json response from make track request

    Returns:
            artist_uri :
            artist_name :
    """
    artist_uri = track_information["artists"][0]["uri"].split(":")[2]

    artist_name = track_information["artists"][0]["name"]

    return (artist_uri, artist_name)


def run_api():
    """
    Runs the main program to create an expanded genre dataframe based
    """
    all_year_streaming_df = run_data_handling()
    expanded_genres_dataframe = pull_song_genre(all_year_streaming_df)
    return all_year_streaming_df, expanded_genres_dataframe


if __name__ == "__main__":
    run_api()
