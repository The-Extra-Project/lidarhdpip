# LidarhdBot 🗺️ 🤖

**Bot application for running geospatial 3D mesh reconstruction algorithms on Compute over Data framework.**

<p align="left">
 <a href="https://github.com/The-Extra-Project/Lidarhdpip/blob/dev-adding-v0.1/LICENSE.md" alt="License">
 <img src="https://img.shields.io/badge/license-MIT-green" />
   </a>

  <a href="https://github.com/The-Extra-Project/Lidarhdpip/releases" alt="Release">
        <img src="https://img.shields.io/github/v/release/The-Extra-Project/lidarhdpip?display_name=tag" />
  </a>
 <a href="https://github.com/The-Extra-Project/lidarhdpip/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/The-Extra-Project/lidarhdpip" />
    </a>
    <a href="https://img.shields.io/github/downloads/The-Extra-Project/lidarhdpip/total">
        <img src="https://img.shields.io/github/downloads/The-Extra-Project/lidarhdpip/total" alt="total downloads">
    </a>
    <a href="https://github.com/The-Extra-Project/lidarhdpip/actions/workflows/test-docker-build.yml" alt="Test deployment">
        <img src="https://github.com/The-Extra-Project/lidarhdpip/actions/workflows/test-docker-build.yml.yml/badge.svg" />
    </a>
    <a href="https://www.extralabs.xyz/">
        <img alt="Extra labs website" src="https://img.shields.io/badge/website-theextralabs.xyz-red">
    </a>
    <a href="https://twitter.com/intent/follow?screen_name=lab_dao">
        <img src="https://img.shields.io/twitter/follow/lab_dao?style=social&logo=twitter" alt="follow on Twitter">
    </a>
    <a href="https://discord.gg/Qmqf2U4Y9Y" alt="Discord">
    <img src="https://dcbadge.vercel.app/api/server/Qmqf2U4Y9Y" />
    </a>
</p>


## Stack:

- **Serverless messaging using**: [upstash]() and [AWS lambda]().

- **rendering visualization using**: [Streamlit]().

- **compute over Data using** [bacalhau]():

- **decentralised storage on top of**[web3.storage]:

- **bot service running on top of**[discord.py]:  

## packages description:


1. [Bots](./bots/): Package for discord bot logic and commands which integrates with kafka and eventually AWS.

2. [aws_deployment](./aws_deployment/): Scripts to deploy the necessary infrastructure on registered AWS cloud.

3. [visualization](./visualization/): This is the rendering app written in streamlit that shows the result once the mesh reconstruction job is completed.

## Build instructions/Setup:

### 1. Locally running the bot:

1. We need to set following enviornment variables 
    - For the kafka messaging service. the reference env file is defined in the `.env.example` [here](./.env.example). 
    - Then define the discord configuration in the config.json in 'bots/Discord/config.json', by following the steps defined [here](https://github.com/topics/discord-bot-template).
    - Setup the personal [web3.storage]() account format and define the access token in the .env file.


2. Then build the container application by running the docker-compose file: 
```
cocker compose build 
```

3. Go to the corresponding channel for which you've added the code and then call the functions as defined by the #API section.


### 2. On cloud instance (AWS): 

1. Setup the awscli parameters (i.e account and access token) in the env variable.  

2. Then run the scripts as defined below.
```sh
cd aws_deployment/ && cdk synth
# if its for the first time , you will be prompted to run the following command also
cdk bootstrap
```

- Follow the instructions in the [readme](./aws_deployment/README.md) of the aws_repository in order to provide the necessary permissions to your account in order to address errors.


5. Store the files on web3.storagefrom where you want to fetch the mapping format (shape/obj files). we have stored the reference files in [data/](./datas/) . and then keep the reference cid generated for the user as parameter to pass for generating the  reconstruction job. 
    - for more detials regarding the files latest version, checkout the following
        - https://geoservices.ign.fr/lidarhd
        - https://pcrs.ign.fr/version3

### API's

discord bot api
```markdown
/circum job_point <<Xcoordiante>> <<Ycoordinate>> <<ipfs_shp_file>> <<ipfs_pipeline_template_file>> : runs the reconstruction job for the given point coordinate and returns the job id.

/circum get_status <<job_id>>: checks status of the reconstruction job with given id generated.

/circum result <<job_id>>: fetches the result (laz file cid) once the job is completed.

/circum visualize <<ipfs_cid>> <<Xoordinate>>  <<Ycoordinates>> :  generated laz file visualization link.
```


# Detailled pipeline of the application working process:


## Credits 

-  [bert lidar rendering pipeline](https://github.com/bertt/nimes): For the description concerning the geosptial data reconstruction algorithms. 

- [Dockerised discord bot template](https://github.com/): Template for running discord bot in docker container.
 

