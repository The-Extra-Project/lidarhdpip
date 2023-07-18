import pytest
from fastapi.testclient import TestClient
import logging
from georender import app


testclient = TestClient(app)


# test to be verified and completed.
# get_tile_url_and_fname_from_polygon
# get_tile_url_and_fname
# generate_pdal_pipeline
# run_georender_pipeline


# 806527.23,6301959.36
# arena of nimes : 43.83494159325771, 4.359621254507554

def test_get_url_fname_from_polygon():
    response = testclient.get("/api/georender/tilePolygon/", params={
        "lattitude_max": "43.83494159325771", "lattitude_min": "43.23", "longitude_max": "4.359621254507554", "longitude_min": "4.21", "fp_cid":"TA_diff_pkk_lidarhd.shp"
    })

    assert response.status_code == 200
    assert response.json() == {
        "laz_path": "",
        "fname": "dirname.7z",
        "dirname": "dirname"
    }


def test_get_tile_url_and_fname():
    response = testclient.get("/api/georender/tilePoint", params= {
        "Xcoord": "43.83494159325771", "Ycoord":"4.359621254507554", "fp_cid": "TA_diff_pkk_lidarhd.shp"
    })

    assert response.status_code == 200
    
    # assert response.json() == {
    #     ""
        
    # }
    
    
def test_generate_pdal_pipeline():
    response = testclient.post("/api/georender/generate_pdal_pipeline", params={
     "dirname": "./datas"   
    })
    assert response.status_code == 200