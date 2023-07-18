import argparse
import geopandas as gpd
import json
from shapely.geometry import Polygon, LineString, Point
import os
from subprocess import run
import requests
from web3StoragePackage import API 
import shutil
import sys
from dotenv import load_dotenv
from pyproj import Transformer  
from subprocess import check_call
from typing import Iterator
from subprocess import run
load_dotenv()
import logging

global w3
w3 = API(os.getenv("WEB3_TOKEN"))

def create_bounding_box(latitude_max: float, lattitude_min: float, longitude_max: float, longitude_min: float, cid_file: str):
    """
    Create a bounding box from 4 coordinates
    """
    return Polygon([(longitude_min, lattitude_min), (longitude_max, lattitude_min), (longitude_max, latitude_max), (longitude_min, latitude_max), (longitude_min, lattitude_min)])

def get_tile_url_and_fname_from_polygon(lattitude_min, lattitude_max, longitude_max , longitude_min, cid_file:str = 'https://bafybeih4m6x6oxaojzfr27czxjbyhivduqlwj35jfczdvmawr2y6gsgonu.ipfs.w3s.link/TA_diff_pkk_lidarhd.shp' ):
    """
    function to return the file format in tile and directory from the polygon section
    
    """
    
    #fp_cid:str = "https://bafybeih4m6x6oxaojzfr27czxjbyhivduqlwj35jfczdvmawr2y6gsgonu.ipfs.w3s.link/TA_diff_pkk_lidarhd.shp" 
    
    print( "Running with lat_max={}, lat_min={}, long_max={}, long_min={}, cid_file={}".format( lattitude_max, lattitude_min, longitude_max, longitude_min, cid_file ) )

    # here the file is stored already in the web3 storage along w/ the details like the time of upload .
    ## this needs to be modified to include possiblity 
    #cid_file = w3.post_upload(fp_cid)
    fileReader = requests.get(cid_file, allow_redirects=True)

    data = gpd.read_file(cid_file)
    
    polygonRegion = create_bounding_box(lattitude_max,lattitude_min,longitude_max,longitude_min)
    out = data.intersects(polygonRegion)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]#.replace("$","\$")#.replace("\\\\","\\")
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    return laz_path, fname, dirname


def get_tile_url_and_fname(coordX:float, coordY:float, fp_cid:str):
    """
    operates the algorithm in order to create tile (corresponding to the given point) along with the filename
    coordX/Y: coordinates (in real number as degree) for the given region
    
    
    """
    

    
    print( "Running with X={}, Y={}".format( coordX, coordY ))

    shp_file = requests.get(fp_cid)
    data = gpd.read_file(shp_file.content)
    transformer = Transformer.from_crs( 'EPSG:4326', 'EPSG:2154' )
    coordX, coordY = transformer.transform( coordX, coordY )

    center = Point(coordX,coordY)

    out = data.intersects(center)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    return laz_path, fname, dirname

def get_user_files_recent(timeline):
    
    """
    it gets the CID's and the filepaths of the given user, 
    this gives the output of listed files , with the decreasing order to storing the file. 
    timeline: its the optional parameter that defines the timeline before the current time (in unix sec) in order to store the details
    """
    
    return w3.user_uploads(timeline)

def generate_pdal_pipeline( dirname ):
    """
    developing the pdal pipeline specified by json template, this file comboned with the final resulting laz archive will be combined to get the tile
    dirname: is the directory there the user has stored the corresponding rendered files (shp and resulting las).
    """
    
    
    with open("./pipeline_template.json", 'r') as file_pipe_in:
        file_str = file_pipe_in.read()
    
    pdal_pipeline = json.loads( file_str )


    file_list = os.listdir( dirname )

    def_srs = "EPSG:2154"

    # Builds the list of dicts and filetags ( fname without ext )
    ftags = []
    las_readers = []
    for fname in file_list:
        tag = fname[:-4]
        ftags.append( tag )
        las_readers.append( { "type": "readers.las", "filename": fname, "tag": tag, "default_srs":def_srs } )
    

    
    for ftag in ftags:
        pdal_pipeline['pipeline'][0]['inputs'].insert( 0, ftag )
    
    
    ## inserting las file readers dicts:
    
    for las_reader in las_readers:
        pdal_pipeline['pipeline'].insert( 0, las_reader )
    
    with open( "./pipeline_gen.json", 'w') as file_pipe_out:
        pipeline_objects = json.dump( pdal_pipeline, file_pipe_out )
        file_pipe_out.write(pipeline_objects)
        file_cid = w3.post_upload(file_pipe_out)
        
    
    
    return file_cid

    
def run_georender_pipeline_point():
    """ 
    this merges the various .laz file (from the tile url and fname) and then extracts and then returns the final point cloud file in the form of.las file (which will be stored in the decentralised cloud).
    
    cid_filepath: this is the url of the shp file (currentmy hardcoded).
    coordX: longitude parameter
    coordY: lattitude parameter
    userprofile: given username in the twitter (used for the differentiation on the mainnet).
    
    
    """
    args = argparse.ArgumentParser(description="runs the georender pipeline based on the given geometric point")
    args.add_argument("coordX")
    args.add_argument("coordY")
    args.add_argument("userprofile")
    

    laz_path, fname, dirname = get_tile_url_and_fname(args.coordX, args.coordY, args.userprofile )
    
    userprofile = "toto"
    ## creating the destination profile
    
    with open("./profile_template.json", 'r') as file_template_in:
        rendered_file = file_template_in.read()
    
    template_cid = w3.post_upload(rendered_file)
    
    ## this function refers the fils from the local storage for now: 
    os.mkdir("../data/"+ userprofile)
    
    # check in case if file is not downloaded in the local directory.
    if not os.path.isfile( fname ):
        check_call( ["wget", "--user-agent=Mozilla/5.0", laz_path] )

    # extraction
    check_call(["7z", "-y", "x", fname] )
    
    generate_pdal_pipeline(dirname=dirname)
    ## storing the details of the mkdir 
    os.mkdir( dirname + userprofile )
    # todo : There should be further doc and conditions on this part
    #        Like understanding why some ign files have it and some don't
    # In case the WKT flag is not set :
    for laz_fname in os.listdir( '.' ):
        f = open( laz_fname, 'rb+' )
        f.seek( 6 )
        f.write( bytes( [17, 0, 0, 0] ) )
        f.close()
    check_call( ["pdal", "pipeline", "../pipeline_gen.json"] )
    shutil.move( 'result.las', '../result.las' )
    
    
def run_georender_pipeline_polygon():
    
    args = argparse.ArgumentParser(description="runs the georender pipeline for the given bounded region defined by the points")
    args.add_argument("lattitude_min") # lattitude_min,, , longitude_max
    args.add_argument("lattitude_max")
    args.add_argument("longitude_min")
    args.add_argument("longitude_max")
    
    laz_path, dirname, filename =  get_tile_url_and_fname_from_polygon(args.lattitude_min, args.lattitude_max, args.longitude_min, args.longitude_max)


    # remaining as same as the previous function:


def call_function(function_name, params: list[str]):
    print(sys.argv)
    if function_name == "run_georender_pipeline":
        run_georender_pipeline_point(params)                            
    elif function_name == "run_georender_pipeline_polygon":
            pass
            

"""
way of invoking this parameters

python3 georender <<function-name>> [params]
"""   
def main(cliargs:any=None):
    call_function("run_georender_pipeline_point",cliargs)
    
if __name__ == "__main__":
    ## parameters that are to be added : coordX, coordY, 
    main(sys.argv)
   