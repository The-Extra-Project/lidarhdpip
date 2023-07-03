import pytest
from fastapi.testclient import TestClient

from streamlit_app import app


testclient = TestClient(app)

# 806527.23,6301959.36
# arena of nimes : 43.83494159325771, 4.359621254507554
def test_get_url_fname_from_polygon():
    response = testclient.get("/tilePolygon", params={
        "lattitude_max": "43.83494159325771", "lattitude_min": "43.23", "longitude_max": "4.359621254507554", "longitude_min": "4.21", "fp_cid":"https://bafybeihufzhj65cicy2b3oofbi2u77gjdpp5573qqlx36pygl4zit2k7pe.ipfs.w3s.link"
    })

    assert response.status_code == 400
    # assert response.json() == {
    #     "url": "https://domain.com/path/to/file.7z",
    #     "fname": "dirname.7z",
    #     "dirname": "dirname"
    # }


def test_get_tile_url_and_fname():
    response = testclient.get("/tilePoint", params= {
        "Xcoord": "43.83494159325771", "Ycoord":"4.359621254507554", "fp_cid": "https://bafybeihufzhj65cicy2b3oofbi2u77gjdpp5573qqlx36pygl4zit2k7pe.ipfs.w3s.link"
    })

    assert response.status_code == 400


