import argparse
import sys
import geopandas as gpd
import json
from shapely.geometry import Polygon, LineString, Point
import os
import requests

def create_bounding_box(latitude_max: int, lattitude_min: int, longitude_max: int, longitude_min: int):
    """
    Create a bounding box from 4 coordinates
    """
    return Polygon([(longitude_min, lattitude_min), (longitude_max, lattitude_min), (longitude_max, latitude_max), (longitude_min, latitude_max), (longitude_min, lattitude_min)])



def get_tile_url_and_fname_from_polygon():
    parser=argparse.ArgumentParser(description="take a bounded box details and produce a 3D tile")
    parser.add_argument("lattitude max")
    parser.add_argument("lattitude min")
    parser.add_argument("longotude max")
    parser.add_argument("longotude min")
    args = parser.parse_args()
    print( "Running with lat_max={}, lat_min={}, long_max={}, long_min={}".format( args.lattitude_max, args.lattitude_min, args.longotude_max, args.longotude_min ) )


    fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    data = gpd.read_file(fp)

    polygonRegion = create_bounding_box(args.lattitude_max, args.lattitude_min, args.longotude_max, args.longotude_min)
    out = data.intersects(polygonRegion)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]#.replace("$","\$")#.replace("\\\\","\\")
    dirname = res["nom_pkk"].to_numpy()[0]
    fname = dirname + ".7z"

    return laz_path, fname, dirname






def get_tile_url_and_fname():
    parser=argparse.ArgumentParser(description="take a gps coordinate and produce a 3Dtile")
    parser.add_argument("coordX")
    parser.add_argument("coordY")
    args=parser.parse_args()
    print( "Running with X={}, Y={}".format( args.coordX, args.coordY ) )

    fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    data = gpd.read_file(fp)

    # todo : how to avoid rewriting too much code between bounding box mode and center mode ?
    # todo : Document input format and pyproj conversion
    # see link 1 ( to epsg codes ), link 2 ( to pyproj doc )
    from pyproj import Transformer
    transformer = Transformer.from_crs( 'EPSG:4326', 'EPSG:2154' )
    coordX, coordY = transformer.transform( args.coordX, args.coordY )

    #center = Point(806527.23,6301959.36) # for demo
    center = Point( float(coordX), float(coordY) )

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
    # Pdal pipeline is specified by a json
    # basically it's a list of filters which can specify actions to perform
    # each filter is a dict
    
    # Open template file to get the pipeline struct 
    with open( "../georender/pipeline_template.json", 'r' ) as file_pipe_in:
        file_str = file_pipe_in.read()
   
    pdal_pipeline = json.loads( file_str )

    # List files extracted
    # Now we don't check extension and validity
    file_list = os.listdir( dirname )

    def_srs = "EPSG:2154"

    # Builds the list of dicts and filetags ( fname without ext )
    ftags = []
    las_readers = []
    for fname in file_list:
        tag = fname[:-4]
        ftags.append( tag )
        las_readers.append( { "type": "readers.las", "filename": fname, "tag": tag, "default_srs":def_srs } )
    
    # Insert file tags in the list of inputs to merge
    # Must be done before next insertion because we know the place of merge filter in the list at this moment
    for ftag in ftags:
        pdal_pipeline['pipeline'][0]['inputs'].insert( 0, ftag )

    # Insert the list of las file readers dicts
    for las_reader in las_readers:
        pdal_pipeline['pipeline'].insert( 0, las_reader )
    
    with open( "pipeline_gen.json", "w" ) as file_pipe_out:
        json.dump( pdal_pipeline, file_pipe_out )


## Pipeline creation
def main():
    # Uses geopanda and shapely to intersect gps coord with available laz tiles files
    # Returns corresponding download url and filename
    laz_path, fname, dirname = get_tile_url_and_fname()

    os.chdir( "../data" ) # So every output file is shared with host
    from subprocess import check_call
    #from subprocess import Popen
    # Download laz tile file from ign
    if not os.path.isfile( fname ): # Causes problem if already existing file is invalid ( like from interrupted download )
        check_call( ["wget", "--user-agent=Mozilla/5.0", laz_path] )
    # Extract it
    check_call( ["7z", "-y", "x", fname] ) 

    generate_pdal_pipeline( dirname )

    # run pdal pipeline with the generated json :
    os.chdir( dirname )
    # todo : There should be further doc and conditions on this part
    #        Like understanding why some ign files have it and some don't
    # In case the WKT flag is not set :
    for laz_fname in os.listdir( '.' ):
        f = open( laz_fname, 'rb+' )
        f.seek( 6 )
        f.write( bytes( [17, 0, 0, 0] ) )
        f.close()
    check_call( ["pdal", "pipeline", "../pipeline_gen.json"] )
    import shutil
    shutil.move( 'result.las', '../result.las' )
#    os.chdir( '..' )

if __name__ == '__main__':
    main()

