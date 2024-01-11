import json
import os

import pandas as pd


from spotify_visualization_project.utils.constants import PROCESSED_DIRECTORY
from spotify_visualization_project.api.spotify_web_api import run_api

# go through data handling steps and call api


def create_directory():
    """
    Checks if the processed data folder exists
    """
    if PROCESSED_DIRECTORY.exists():
        print("Directory already exists")
    else:
        PROCESSED_DIRECTORY.mkdir(parents=True, exist_ok=True)
        print(f"Created {PROCESSED_DIRECTORY}")


def to_excel(streaming_dataframe, genre_dataframe):
    """
    Pandas DataFrame to excel

    Inputs:

    Returns: None
    """
    create_directory()

    streaming_path = PROCESSED_DIRECTORY / "streaming_dataframe.csv"
    genre_path = PROCESSED_DIRECTORY / "genre_dataframe.csv"

    streaming_dataframe.to_csv(streaming_path)
    genre_dataframe.to_csv(genre_path)

    print("DataFrames Converted to CSV")


def main():
    """
    Runs the main function
    """
    # runs the data_handling, api call to get track uri list to get genres for
    # tracks listened to and then creates a folder for the cleaned and renamed
    # files within the data folder
    streaming_dataframe, genre_dataframe = run_api()
    to_excel(streaming_dataframe, genre_dataframe)
