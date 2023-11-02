FROM --platform=linux/amd64 python:3.11.1  as build 

WORKDIR /

COPY ./requirements.txt  /usr/src/app/bots/requirements.txt

WORKDIR /usr/src/app/bots/

RUN pip install -r requirements.txt
##env needs to be 
COPY ../.env  ../

COPY . .


FROM build as run

COPY --from=build /usr/src/app/bots/ /usr/src/app/bots/
WORKDIR /usr/src/app/bots/Discord
ENTRYPOINT [ "python3", "circombot.py" ]