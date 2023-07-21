# Georender complete pipeline:

This dockerised image takes the given raw file depicting the geographic file ( in .shp) and then converts it into 3D tile specification, which then will be rendered by the 3D tile rendering service.


## steps to setup:

1. Define the variables as given in the `.env.example`.
2. then build the docker contianer file using the  `docker build -t geo-render .` command.
3. run the docker container using the command `docker run -d -p 8080:8080 geo-render  <name of the function> <coordinate> <username>`.
    - if this is to be run for `run_geometric_pipeline_point`, this will need the (X,Y)coorindate parameter.
    - if this is to be run for `run_geometric_pipeline_polygon`, this will require the coordinates of the polygon in the ranges (i.e (latitude_max: float, lattitude_min: float, longitude_max: float, longitude_min: float)).
 


## API:






