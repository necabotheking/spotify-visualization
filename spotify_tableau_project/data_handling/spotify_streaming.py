import os

import pandas as pd
from utils.constants import YEAR_LST


def read_all_streaming_history():
    """
    Navigates to the data folder and creates lists of files by year to be read in

    Inputs: None

    Returns: streaming_dict (dict): dictionary of dataframes with year of spotify data as the key
    """
    streaming_dict = {}

    mycwd = os.getcwd()

    os.chdir("spotify_tableau_project/data/raw")

    for year in YEAR_LST:
        year_files = [file for file in os.listdir() if year in file]
        df = read_data(year_files)
        streaming_dict[year] = df

    os.chdir(mycwd)

    return streaming_dict


def read_data(year_files):
    """
    Reads the data into a pandas dataframe and concatenates years into the one Pandas DataFrame

    Inputs:
        year_files (lst):
        year (str):

    Returns: streaming_df (Pandas DataFrame)
    """
    streaming_lst = []

    for file in year_files:
        df = pd.read_json(file)
        formatted_df = format_dataframe(df)
        streaming_lst.append(formatted_df)
    streaming_df = pd.concat(streaming_lst)
    return streaming_df


def format_dataframe(dataframe):
    """
    Returns the Pandas DataFrame formatted in-place

    Inputs: dataframe (Pandas DataFrame)

    Rturns: dataframe (Pandas DataFrame)
    """
    # checks to see if the dataframe has just podcasts or songs
    dataframe["UniqueID"] = (
        dataframe["master_metadata_album_artist_name"]
        + " : "
        + dataframe["master_metadata_track_name"]
    )
    # remove unnecessary  cols - user_agent_decrypted, ip_addr_decrypted
    # drop columns without a track_uri AND episode_uri
    uri = dataframe["spotify_track_uri"].str.split(":", expand=True)

    dataframe["spotify_uri_clean"] = uri[2]
    # NOTE drop the rows that don't have any data/no URI
    # and drop the podcast episodes

    return dataframe


def create_total_streaming_data(streaming_dict):
    """
    Creates a merged Pandas DataFrame with all of the years

    Inputs:
            streaming_dict (Pandas DataFrame):

    Returns: merged_df (Pandas DataFrame):
    """
    merged_df = pd.concat(streaming_dict.values(), axis=0)
    return merged_df


def main():
    """
    Runs the main functions

    Inputs: None

    Returns: yearly_streaming_dict (dict)
             all_year_streaming_df (Pandas DataFraame)
    """
    yearly_streaming_dict = read_all_streaming_history()
    all_year_streaming_df = create_total_streaming_data(yearly_streaming_dict)

    return yearly_streaming_dict, all_year_streaming_df
