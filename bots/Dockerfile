FROM --platform=linux/amd64 python:3.11.1  as build 

RUN mkdir -p /usr/src/app/discordbot/
COPY requirements.txt  /usr/src/app/discordbot/requirements.txt

WORKDIR /usr/src/app/discordbot/


RUN pip install  --upgrade pip && pip install  -r requirements.txt

## PATH="/root/.local/bin:$PATH"
ENV PATH=" ${PATH}:/root/.local/bin" 



FROM build as run
COPY . /usr/src/app/discordbot/

COPY --from=build /usr/src/app/discordbot/ /usr/src/app/discordbot/

WORKDIR /usr/src/app/discordbot/

CMD [ "python3", "circombot.py" ]