import pytest
import os
from dotenv import load_dotenv
from w3storage import API
import geopandas
from  geopandas import GeoDataFrame
from io import BytesIO

global web3token
web3token =  API(token=os.getenv('WEB3_TOKEN'))
load_dotenv()

def test_setup_web3token():
    print(web3token._auth)
    assert web3token._auth is not None
    
def test_getting_cid_for_file():
    # now finding the directory path 
    filepath = "../georender/datas/TA_diff_pkk_lidarhd.shp"
    #fileobj = geopandas.read_file(filepath)
    
    cid_details = web3token.post_upload('testfile', open(filepath,"rb"))
    print(cid_details)
        