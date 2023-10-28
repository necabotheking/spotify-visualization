import json
import os

import pandas as pd

from spotify_tableau_project.api.spotify_web_api import main

# go through data handling steps and call api


def create_directory():
    """
    Checks if the processed data folder exists
    """
    if os.path.exists("spotify_tableau_project/data/processed"):
        print("Directory already exists")
    else:
        os.mkdirs("spotify_tableau_project/data/processed")
        print("Created spotify_tableau_project/data/processed")


def to_excel(streaming_dataframe):
    """
    Pandas DataFrame to excel
    """
    create_directory()
    mycwd = os.getcwd()
    # should turn each file to excel and dump them into the processed folder
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
