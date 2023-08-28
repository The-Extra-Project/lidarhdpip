"""
frontend for users to access the 3D reconstructed tile and then render it on the browser

"""
import time
import streamlit as st
import os 
from kafka import KafkaConsumer, KafkaProducer
from dotenv import load_dotenv, dotenv_values
from visualizer_component import run_visualization
st.set_page_config(layout="wide")


config = dotenv_values(dotenv_path='../.env')

topic = ['lidarbot_get_visualization']

consumer = KafkaConsumer(
          bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
  auto_offset_reset='earliest',
  consumer_timeout_ms=1000
)

def parse_submit_visualization_documentation() -> list(str):
    consumer.subscribe(topic[0])
    message = consumer.poll(timeout_ms=1000, max_records=1)
    ## now parsing the details for the visualization of the tiles
    if message:
        message = message[0]
        key = message.key
        value = message.value
        data = str(value.decode('utf-8')).split(',')
        print(f"Received data from kafka: {data}")
        tileIpfs = data[0]
        username = data[1]
    return [tileIpfs, username]
        
def render_visualization(Xcoord, Ycoord):
    [tileIpfs, username] = parse_submit_visualization_documentation()
    st.header(f"Visualization for tile {tileIpfs} submitted by {username}")
    
    while st.container():
        # Code to render 3D visualization goes here
        time.sleep(1)
        run_visualization(tilesetIPFS=tileIpfs,Xcoordinate=Xcoord, Ycoordinate=Ycoord)
        

def main():
    st.title("georender: download 3D geospatial database from algorithms running on web3")
    st.text("add your twitter handle name, select the required geo-coordinates and then get your shp file ready")

    with st.sidebar:
        with st.expander("User-details" ,False):
            user_name = st.text_input("account user-name")
        with st.expander("add geo-coordinates", False):
            x_coord = st.text_input("X coordinates")
            y_coord = st.text_input("Y coordinates")

    ## user before needs to set the env variables files.
    with st.button("submit details"):
        try:
            if user_name & x_coord & y_coord:    
                render_visualization(Xcoord=x_coord, Ycoord= x_coord)        
                st.success("Job submitted successfully")
            else:
                st.error("please enter the user name")
        except Exception as e:
            st.error(f"parameters not complete")
            st.stop()

if __name__ == "__main__":
    main()