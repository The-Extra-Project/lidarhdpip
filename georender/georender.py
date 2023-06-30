from fastapi import FastAPI
import sys
import geopandas as gpd
import json
from shapely.geometry import Polygon, LineString, Point
import os
from subprocess import Popen
import requests
from web3StoragePackage import API 
import uvicorn
import py7zr
import io

app = FastAPI()

w3 = API(os.getenv("WEB3_TOKEN"))


def create_bounding_box(latitude_max: float, lattitude_min: float, longitude_max: float, longitude_min: float):
    """
    Create a bounding box from 4 coordinates
    """
    return Polygon([(longitude_min, lattitude_min), (longitude_max, lattitude_min), (longitude_max, latitude_max), (longitude_min, latitude_max), (longitude_min, lattitude_min)])

@app.get("/tilePolygon/")
def get_tile_url_and_fname_from_polygon(lattitude_max:float, lattitude_min:float , longitude_max:float, longitude_min:float, fp_cid:str ):
    print( "Running with lat_max={}, lat_min={}, long_max={}, long_min={}".format( lattitude_max,lattitude_min, longitude_max, longitude_min ) )

    """
    function to return the file format in tile and directory.
    

    lattitude_max: its the floating number defining the lattitude number
    
    """


    #fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    # here the file is stored already in the web3 storage along w/ the details like the time of upload .
    ## this needs to be modified to include possiblity 

    fileReader = requests.get(fp_cid)
    file_data = fileReader.content
    data = gpd.read_file(io.BytesIO(file_data))

    polygonRegion = create_bounding_box(lattitude_max,lattitude_min,longitude_max,longitude_min)
    out = data.intersects(polygonRegion)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]#.replace("$","\$")#.replace("\\\\","\\")
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    return laz_path, fname, dirname


@app.get("/tilePoint")
def get_tile_url_and_fname(coordX:float, coordY:float, fp_cid:str):
    print( "Running with X={}, Y={}".format( coordX, coordY ))

    #fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    ##
    data = gpd.read_file(fp_cid)
    center = Point(coordX,coordY)

    out = data.intersects(center)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    with open("tmp/filepath.txt" + coordX + coordY, "w") as outfile:
       outfile.write(laz_path)
    #with open("filename.txt", "w") as outfile:
    #    outfile.write(fname)
    return laz_path, fname, dirname

@app.post("/generate_pdal_pipeline")
def generate_pdal_pipeline( dirname ):
    # List files extracted (that are stored in the decentralised storage)
    file_list = os.listdir( dirname )

    def_srs = "EPSG:2154"
    
    # Open template file to get the pipeline struct 
    with open( "pipeline_template.json", 'r' ) as file_pipe_in:
        file_str = file_pipe_in.read()
    
    pdal_pipeline = json.loads( file_str )
    
    las_reader = { "type": "reader.las", "filename": "filename.laz", "tag": "filename", "default_srs":def_srs }
    
    pdal_pipeline['pipeline'].insert( 0, las_reader )
    
    with open( "pipeline_gen.json", "w" ) as file_pipe_out:
        json.dump( pdal_pipeline, file_pipe_out )


@app.post("/unzip_files")
def unzip_files(filename: list[str]):
    """
    this unzips the file stored from the get_url_fname.... method and then makes them downlodable on the user browser.

    """
    try:
        for i in filename:
            with py7zr.SevenZipFile( str(i), "r") as z:
                z.extractall(path="/temp"+ str(i))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    uvicorn.run("main:app",log_level='info', port=1000)
