# Lidarbot/Visualization:

This application package renders 3D view of the reconstructed mesh by [bacalhau](../bacalau/) computation result.

## Credits to:
- [discord-bot-template](https://github.com/kkrypt0nn/Python-Discord-Bot-Template). 
- [streamlit-component](https://github.com/streamlit/component-template).

## Tech stack:
1. upstash : for integrating the bot with the kafka service.

## build instructions:
1.  Defining the parameters for the bots:
    - For twitter and kafka provider: provide the parameters as defined by the `.env.example`.
    - `$ cp .env.example .env`
    - then also instantiate a config.json file (as defined by the config-example.json) and then return the result.

    - for discord:
        - the details are defined in the [readme](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/README.md) of the python discord bot template.
        
        - invite your bots by replacing the generated parameters using the url given [here](https://discord.com/oauth2/authorize?&client_id=1138054674696650842&scope=bot+applications.commands&permissions=2048):  




2. Run the docker container.


For more information regarding the deployment on cloud, checkout the [aws_deployment](../aws_deployment/) setup.