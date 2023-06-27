"""
frontend for users to download the formatted sns file

usage:
- https://github.com/tulasinnd/Twitter-scraping-with-snscrape-and-streamlit/blob/main/Twitter_Scraper.py
for the idea of using snscrape.

"""
import time
import streamlit as st
#import snscrape.modules.twitter as sntwitter
import pandas as pd
import requests
from producers.twitter_producer import produce_Tweet_details
from .tweepy import TwitterAccess
import os 


resulting_tweets = pd.DataFrame()
request_number = 0

## stores the maps along.


def latency(sec: int):
    """
    introduces the latency in seconds.
    """

    timedelay = st.empty()
    for i in range(sec):
        timedelay.text(f"waiting for {sec-i} seconds")
        time.sleep(1)
    return False


def submitJob(request_number, params):
    """
    submits the job to the kafka queue.
    """
    button = st.button("submit job")
    if button:
        try:
            produce_Tweet_details()
            st.success("Job submitted successfully")
        except Exception as e:
            print(e)
            st.error("kafka error: job didnt got submitted ")
    

def get_env_variables():
  """Gets the env configuration variables."""
  env_variables = {}
  for key, value in os.environ.items():
    env_variables[key] = value
  return env_variables




def main():
    st.title("georender: download 3D geospatial database from algorithms running on web3")
    st.text("add your twitter handle name, select the required geo-coordinates and then get your shp file ready")

    with st.sidebar:
        with st.expander("User-details" ,False):
            user_name = st.text_input("user-name")
            start_time = st.time_input("start time for tweet")
            end_time = st.time_input("end time for the tweet timeline")
            count = st.slider('How many tweets to scrape', 0, 1000, 5)
        with st.expander("add geo-coordinates", False):
            x_coord = st.text_input("X coordinates")
            y_coord = st.text_input("Y coordinates")

    params= [x_coord, y_coord]
    ## user before needs to set the env variables files.
    env_vars = get_env_variables()
    with st.button("submit details"):
        try:
            if user_name:
                submitJob(request_number, params)
                tweepyObject = TwitterAccess(env_vars["ACCESS_TOKEN"], env_vars["ACCESS_TOKEN_SECRET"], env_vars["CONSUMER_KEY"], env_vars["CONSUMER_SECRET"])
                tweepyObject.write_tweets(x_coord + y_coord)
                st.success("Job submitted successfully")
            else:
                st.error("please enter the user name")
        except Exception as e:
            st.error(f"Too many requests")
            st.stop()


if __name__ == "__main__":
    main()