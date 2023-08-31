"""
frontend for users to access the 3D reconstructed tile and then render it on the browser

"""
import time
import streamlit as st
from streamlit import exception
import os 
from dotenv import load_dotenv, dotenv_values
from visualizer_component import run_visualization
st.set_page_config(layout="wide")

config = dotenv_values(dotenv_path='../.env')


def render_visualization(Xcoord, Ycoord, _tileIpfs, _username):
    [tileIpfs, username] = [_tileIpfs , _username]
    st.text(f"Visualization for tile {tileIpfs} submitted by {username}")
    
    while st.container():
        # Code to render 3D visualization goes here
        time.sleep(1)
        run_visualization(tilesetIPFS=tileIpfs,Xcoordinate=Xcoord, Ycoordinate=Ycoord, username=_username)
    

def render_download_button(tileIpfs, user_name, x_coord, y_coord):
    st.header("Download your 3D tile")
    try:
        if len(user_name) and len(x_coord) and len(y_coord):    
            render_visualization(Xcoord=x_coord, Ycoord= x_coord, _tileIpfs=tileIpfs, _username=user_name)        
            st.success("Job submitted successfully")
        else:
            st.error("please enter the user name")
    except RuntimeError as e:

            st.error(f"exception")
            st.exception(e)
            st.stop()    

def main():
    st.title("georender: download 3D geospatial database from algorithms running on web3")
    st.text("add your twitter handle name, select the required geo-coordinates and then get your tilerendered")

    with st.sidebar:
        with st.expander("User-details" ,False):
            user_name = st.text_input("account user-name", value="toto", key="User_name")
            tile_ipfs = st.text_input("ipfs uploaded version of tile files", value="bafybeibbtseqjgu72lmehn2y2b772wvr36othnc4rpzu6z3v2gfsjy3ew4", key="Tile_ipfs")

        with st.expander("add geo-coordinates", False):
            x_coord = st.text_input("X coordinates", value=43,key="X_coord")
            y_coord = st.text_input("Y coordinates", value=32, key="Y_coord")

    clicked_button = st.button("submit", key="Submit_button")
    if clicked_button:
        render_download_button(tileIpfs=tile_ipfs,user_name=user_name,x_coord=x_coord,y_coord= y_coord)
            


        

if __name__ == "__main__":
    main()