
# New pipeline instructions

docker override entrypoint for debug :
```bash
docker run -it --entrypoint=/bin/bash myimagename
```

## How to use georender

```bash
# if first run build docker image
cd georender
docker compose build 
cd ..

# Georender docker image id : get last georender image id and assign to a shell variable
GEOID=$(sudo docker images | grep georender | sed -e 's/\s\+/,/g' | cut -d ',' -f 3)

# run in a container with gps coordinates
docker run -v $(pwd)/data:/usr/src/app/data --rm $GEOID 43.2946 5.3695
```

## How to use las to tiles converter

note : fixed dockerfile by adding :bullseye to python-slim image because the laszip package isn't available in last lts repositories

```bash
# if first run build docker image from py3dtiles
cd py3dtiles
docker build . -t py3dtiles -f docker/Dockerfile
cd ..

# Py3dtiles docker image id : get last py3dtiles image id and assign to a shell variable
TILERID=$(sudo docker images | grep py3dtiles | sed -e 's/\s\+/,/g' | cut -d ',' -f 3)
LAS_FILE=result.las
TILE_OUTDIR=3dtiles

# Run in the container with result las file from georender
docker run -it --rm --mount type=bind,source="$(pwd)/data",target=/app/data/ $TILERID convert $LAS_FILE --out $TILE_OUTDIR
```

## How to use visualiser

built image from 3dTilesRendererJS and a simple node js docker

```bash
# if first run build docker image from 3dTilesRendererJS and base node image
docker build . -t 3dtilesviz -f docker/Dockerfile

# TilesViz docker image id : get last 3dtilesViz image id and assign to a shell variable
TVIZID=$(sudo docker images | grep 3dtilesviz | sed -e 's/\s\+/,/g' | cut -d ',' -f 3)

# Run the container with tiles folder from py3dtiles to serve visualisation
docker run -v $(pwd)/data:/usr/src/app/3DTilesRendererJS/data -p 127.0.0.1:9080:9080 -it --rm $TVIZID
```

when the image is launched, go to the following address : http://localhost:9080/example/dev-bundle/index.html

If the page is not found look in the terminal, the docker image output should indicate when the code is built and ready to run.
