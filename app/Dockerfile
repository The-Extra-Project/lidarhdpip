FROM python:3.11.1

RUN mkdir -p  /usr/src/app/discordbot/

COPY ./pyproject.toml  /usr/src/app/discordbot/pyproject.toml

WORKDIR /usr/src/app/discordbot/

RUN curl -sSL https://install.python-poetry.org | python3 - && export PATH="/root/.local/bin:$PATH" && poetry install 

WORKDIR /

ADD ./src/bots/Discord /usr/src/app/discordbot/


ENTRYPOINT [ "python3", "/usr/src/app/discordbot/circombot.py" ]