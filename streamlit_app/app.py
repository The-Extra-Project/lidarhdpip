"""
frontend for users to access the 3D tile of the coordinate and then download it

"""
import time
import streamlit as st
import pandas as pd
import requests
from kafka.producers.twitter_producer import produce_Tweet_details
from kafka.model import TwitterProducerMessage
from twitterbot.tweepy import TwitterAccess

import os 
from web3storage.package import API
import py3dtiles
## this is the format of storing the parameters 
resulting_tweets = pd.DataFrame()
request_number = 0

st.set_page_config(layout="wide")

def latency(sec: int):
    """
    introduces the latency in seconds.
    """

    timedelay = st.empty()
    for i in range(sec):
        timedelay.text(f"waiting for {sec-i} seconds")
        time.sleep(1)
    return False


def submitJob(request_number: int, params: TwitterProducerMessage) -> bool:
    """
    submits the job to the kafka queue.

    input: 
    request_number: is the optional identification job request.
    params: is the input parameters that are to be passed to send the requests. 


    """
    button = st.button("submit job")
    if button:
        try:
            produce_Tweet_details()
            st.success("Job submitted successfully")
            return True
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
            user_name = st.text_input("account user-name")
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
                ## now storing the corresponding result of the execution in the cache.
                ## for now i am trying to do that using ipfs.

                


                st.success("Job submitted successfully")
            else:
                st.error("please enter the user name")
        except Exception as e:
            st.error(f"Too many requests")
            st.stop()


if __name__ == "__main__":
    main()