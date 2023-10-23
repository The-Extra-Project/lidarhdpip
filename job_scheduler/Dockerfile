FROM  ubuntu:22.04 as build 


WORKDIR /app
RUN apt-get update && apt-get install -y python3-dev pip

COPY requirements.txt .

RUN apt-get update 

RUN pip install -r requirements.txt

COPY .  .

FROM build as run

COPY --from=build /app/ /app/

CMD [ "python3", "/app/main.py" ]

