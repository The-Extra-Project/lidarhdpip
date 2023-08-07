# lidarhd bot app:

This package consist of various UI iplementations for : 
- getting the user input: via discord bot as well as twitterbot
- rendering the output result (via streamlit UI).


## build instructions:
1.  Defining the parameters for the bots:
    - For twitter and kafka provider: provide the parameters as defined by the `.env.example`.
    - `$ cp .env.example .env`
    - then also instantiate a config.json file (as defined by the config-example.json) and then return the result.

2. Run the docker container.