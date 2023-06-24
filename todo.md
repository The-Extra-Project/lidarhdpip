
## Todo day 3

### [] write run.sh in python

 [x] refactor in python general code struct from run.sh and main.py
( [] test use wget in python ) to speed up, use already downloaded tile.7z
 [x] test use 7z in python

### [x] get folder extract name

 [x] ls ( os.listdir dirname ( got dirname from filename - 7z ) )

### [] Json pdal pipeline generate

structure :
 - pipeline 
  - reader.laz for every file .laz
  - filter : merge
  - optionnal : filter : assign ( l'ex de nimes applique des seuils sur les coords )
  - filter : crop ( si bounding box spécifiée )
  - writer.las to output a result.las

 [x] load a template json for boilerplate params
 [] insert variable params ( list of files to read and merge from previous step )
 [x] write json file

start with mock file struct
cropped las files to speed up tests

 - See later :
Si la zone dans result.las est trop grande pour tenir en memoire avec gocesiumtiler
faire un deuxieme pipeline de crop avec des chunk qui fit dans la memoire dispo

### [] commit changes

### [] generate tile with result.las

 - [] use gocesiumtilegene from python script

### [] visualize cesium tile

 - [] check install
 - [] make minim app with 3dtilerendererjs
 - [] test with mock tile ?
 - [] test with generated tile

### [] write visualizer docker

### Cleanup, improve

#### add meaningful error message in every step

#### add verbosity

#### document better

#### check gps coord input

### Also

#### Arles cloud : why different coord from OSM ? ( checked with nimes )

#### Vps requirement




## Dhruv Side: 


Simple workflow : 

1.input (coordinates, identification) --> Event-Consumer (Confluent-kafka-serverless) --> bacalau-cli (with the docker image).



tasks:

- [X] Containerize the docker image (Dockerfile-pdal and georender), change the API endpoints and standardise with tests.
- [X] Similar w/ cgal
- [X]  bacalau deployment script 
- [] confluent kafka streaming
- [ ] full demo.





