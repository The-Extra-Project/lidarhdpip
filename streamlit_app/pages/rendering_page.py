from py3dtiles.tileset.tileset import TileSet
import w3storage
import streamlit as st
from pathlib import Path
from subprocess import run, Popen
from dotenv import load_dotenv
st.set_page_config(layout="wide")
import os
load_dotenv()

w3 = w3storage.API(os.getenv("WEB3_TOKEN"))

def render_output_file(cid: str):
    """
    this renders the 3Dtile file by reading the json pipeline tileset.
    cid: is the storage id of the tileset information
    
    """

    st.title("rendered map")
    st.markdown("checkout the output tileset map from the uploaded file")
    rendertile = st.button("render the tileset")
    
    
    datapath = os.chdir("../dir")
    shpfile = open(datapath, "w")
    # = requests.get(cid).content
    run("wget " + cid, verbose=True)
    
    if rendertile:
        render_tiles_path = st.file_uploader("select the downloaded 3Dtileset format files")

        
        
        if upload_tiles is not None:
            tileset = TileSet.from_file()
        
    
    
    
    
        