import os
import pandas as pd

from spotify_visualization_project.utils.constants import DATA_DIRECTORY


def read_all_streaming_history() -> dict:
    """
    Navigates to the data folder and creates lists of files by year to be read in

    Inputs: None

    Returns: streaming_dict: dictionary of Pandas DataFames with year of spotify data as the key
    """
    year_lst = [*range(2018, 2024)]

    streaming_dict = {}

    for year in year_lst:
        year_files = [
            os.path.join(DATA_DIRECTORY, file)
            for file in os.listdir(DATA_DIRECTORY)
            if str(year) in file
        ]
        formatted_dataframe = read_data(year_files)
        streaming_dict[year] = formatted_dataframe

    return streaming_dict


def read_data(year_files: list[str]) -> pd.DataFrame:
    """
    Reads the data into a pandas dataframe and concatenates years into the one Pandas DataFrame

    Inputs:
        year_files (lst): List of json files of spotify streaming data

    Returns: streaming_df: Pandas Dataframe of concatenated data from one year of spotify streaming data
    """
    streaming_lst = []

    for file in year_files:
        df = pd.read_json(file)
        formatted_df = format_dataframe(df)
        streaming_lst.append(formatted_df)
    streaming_df = pd.concat(streaming_lst)
    return streaming_df


def format_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the Pandas DataFrame formatted in-place

    Inputs:
            dataframe: unformatted dataframe of spotify streaming data

    Returns: dataframe: formatted dataframe of spotify streaming data
    """
    dataframe["uniqueID"] = (
        dataframe["master_metadata_album_artist_name"]
        + " : "
        + dataframe["master_metadata_track_name"]
    )

    # drop unnecessary columns
    dataframe = dataframe.drop(
        [
            "user_agent_decrypted",
            "ip_addr_decrypted",
            "episode_name",
            "episode_show_name",
            "spotify_episode_uri",
        ],
        axis=1,
    )

    uri = dataframe["spotify_track_uri"].str.split(":", expand=True)

    dataframe["spotify_uri_clean"] = uri[2]

    dataframe = dataframe.dropna(subset=["spotify_track_uri"])

    return dataframe


def create_total_streaming_data(streaming_dict: dict) -> pd.DataFrame:
    """
    Creates a merged Pandas DataFrame with all of the years

    Inputs:
            streaming_dict: dictionary of 2018 - 2023 spotify streaming data

    Returns: merged_df: Pandas DataFrame of 2018 - 2023 spotify streaming data
    """
    merged_df = pd.concat(streaming_dict.values(), axis=0)
    return merged_df


def run_data_handling():
    """
    Runs the main functions and returns the 2018 - 2023 steaming dataframe

    Inputs: None

    Returns: yearly_streaming_dict (dict)
             all_year_streaming_df (Pandas Frame)
    """
    yearly_streaming_dict = read_all_streaming_history()
    all_year_streaming_df = create_total_streaming_data(yearly_streaming_dict)

    return all_year_streaming_df


if __name__ == "__main__":
    run_data_handling()
