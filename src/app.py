"""
frontend for users to download the formatted sns file

credits to:
- https://github.com/tulasinnd/Twitter-scraping-with-snscrape-and-streamlit/blob/main/Twitter_Scraper.py

for the idea of using snscrape
"""

import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from typing import Mapping
from producers.twitter_producer import produce_Tweet_details
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
    try:
        while latency(100):
            print("waiting for pushing the "+ str(request_number) + " request" + "to queue")
        
        produce_Tweet_details(request_number,params)     

    #   resulting_tweets
        st.write("job submitted")
    except Exception as e:
        st.error(f"Too many requests")
        st.stop()
        
if __name__ == "__main__":
    main()