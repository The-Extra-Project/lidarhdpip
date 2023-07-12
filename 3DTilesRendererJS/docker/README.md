
# Visualisation tool dockerized

## Usage

### Build image with :

#### From node app dockerize tuto :
docker build . -t <your username>/node-web-app

#### From py3dtiles :
You must run the following command in the root folder of the repository
```bash
docker build . -t py3dtiles -f docker/Dockerfile
```

### How to use the docker image

#### From py3dtiles :
The docker image has a volume on `/app/data/` and the entrypoint is directly the command `py3dtiles`.

##### Examples

Display the help
```bash
docker run -it --rm py3dtiles --help
```

Convert a file into 3d tiles
```bash
docker run -it --rm \
    --mount type=bind,source="$(pwd)",target=/app/data/ \
    --volume /etc/passwd:/etc/passwd:ro --volume /etc/group:/etc/group:ro --user $(id -u):$(id -g) \
    py3dtiles \
    convert <file>
```

NOTE:

- the `--mount` option is necessary for docker to read your source data and to write the result. The way it is written in this example only allows you to read source files in the current folder or in a subfolder
- This line `--volume /etc/passwd:/etc/passwd:ro --volume /etc/group:/etc/group:ro --user $(id -u):$(id -g)` is only necessary if your uid is different from 1000.
