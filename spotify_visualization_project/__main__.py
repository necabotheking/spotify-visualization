"""
Main function for the Spotify Web API Project 
"""

from spotify_visualization_project.data_handling.spotify_streaming import run_data_handling
from spotify_visualization_project.api.spotify_web_api import run_api
from spotify_visualization_project.data_handling.streaming_to_excel import main





def main():
    """
    
    """
    pass
    # streaming_dataframe = run_data_handling
    # streaming_dataframe, genre_dataframe = run_api(streaming_dataframe)
    # main(streaming_dataframe, genre_dataframe)


if __name__ == "__main__":
    main()