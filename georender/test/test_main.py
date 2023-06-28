import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from ..main import app


testclient = TestClient(app)

# 806527.23,6301959.36
# arena of nimes : 43.83494159325771, 4.359621254507554
@pytest.mark.anyio
async def test_get_url_fname_from_polygon():
    response = testclient.get("/tilePolygon", params={
        "lattitude_max": "43.83494159325771", "lattitude_min": "43.23", "longitude_max": "4.359621254507554", "longitude_min": "4.21"
    })

    assert response.status_code == 400

async def test_get_tile_url_and_fname():
    response = testclient.get("/tilePoint", params= {
        "Xcoord": "43.83494159325771", "Ycoord":"4.359621254507554"
    })

    assert response.status_code == 400


    