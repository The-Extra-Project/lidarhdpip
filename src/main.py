import argparse
import sys
import geopandas as gpd
import json
from shapely.geometry import Polygon, LineString, Point
import os
from subprocess import Popen

def get_tile_url_and_fname():
    parser=argparse.ArgumentParser(description="take a gps coordinate and produce a 3Dtile")
    parser.add_argument("coordX")
    parser.add_argument("coordY")
    args=parser.parse_args()
    print( "Running with X={}, Y={}".format( args.coordX, args.coordY ) )

    fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    data = gpd.read_file(fp)
    #center = Point(806527.23,6301959.36) # for demo
    center = Point(float(args.coordX),float(args.coordY))

    out = data.intersects(center)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]#.replace("$","\$")#.replace("\\\\","\\")
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    #with open("filepath.txt", "w") as outfile:
    #    outfile.write(laz_path)
    #with open("filename.txt", "w") as outfile:
    #    outfile.write(fname)
    return laz_path, fname, dirname

def generate_pdal_pipeline( dirname ):
    # List files extracted
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


## Pipeline creation
def main():
    # Uses geopanda and shapely to intersect gps coord with available laz tiles files
    # Returns corresponding download url and filename
    laz_path, fname, dirname = get_tile_url_and_fname()

    # Download laz tile file from ign
    #Popen( ["wget", "--user-agent=Mozilla/5.0", laz_path] )
    # Extract it
    Popen( ["7z", "x", fname] ) 

    generate_pdal_pipeline( dirname )

if __name__ == '__main__':
    main()

