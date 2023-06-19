import argparse
import sys
import geopandas as gpd
import json
from shapely.geometry import Polygon, LineString, Point
import os

## Pipeline creation
def main():

    parser=argparse.ArgumentParser(description="take a gps coordinate and produce a 3Dtile")
    parser.add_argument("coordX")
    parser.add_argument("coordY")
    args=parser.parse_args()

    fp = "/usr/src/app/georender/datas/TA_diff_pkk_lidarhd.shp"
    data = gpd.read_file(fp)
    center = Point(806527.23,6301959.36)
    center = Point(float(args.coordX),float(args.coordY))

    out = data.intersects(center)
    res = data.loc[out]
    laz_path = res["url_telech"].to_numpy()[0]#.replace("$","\$")#.replace("\\\\","\\")
    fname = res["nom_pkk"].to_numpy()[0] + ".7z"

    # # Actually the pipeline is useless beacause it 
    # pipeline = [
    #     {
    #         "type": "readers.las",
    #         "filename": fname ,
    #             "tag": "laz",
    #          "default_srs":"EPSG:2154"
    #     },
    #     {
    #       "type": "writers.las",
    #       "filename": "result.las"
    #     }
    # ]
    # with open("full_pipeline.json", "w") as outfile:
    #     json.dump(pipeline,outfile)
    with open("filepath.txt", "w") as outfile:
        outfile.write(laz_path)
    with open("filename.txt", "w") as outfile:
        outfile.write(fname)

if __name__ == '__main__':
    main()

