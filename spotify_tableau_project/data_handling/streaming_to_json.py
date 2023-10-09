import os
import pandas as pd
import json
from spotify_tableau_project.api.spotify_web_api import main

# go through data handling steps and call api


def to_json(streaming_dataframe):
    """ """
    pass
    mycwd = os.getcwd()
    # should turn each file to JSON and dump them into the processed folder
    # within the data folder. naming conventions for the files?


# if os.path.exists("spotify_tableau_project/data/processed"):
# os.remove("spotify_tableau_project/data/processed")
# os.makedirs("spotify_tableau_project/data/processed")

# for key, dataframe in streaming_dict:

# filename = f'{key}.json'


def main():
    """
    Runs the main function
    """
    # runs the data_handling, api call to get track uri list to get genres for
    # tracks listened to and then creates a folder for the cleaned and renamed
    # files within the data folder
    main()
