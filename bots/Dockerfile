FROM python:3.11.1

RUN mkdir -p  /usr/src/app/discordbot/

COPY ./pyproject.toml  /usr/src/app/discordbot/pyproject.toml

WORKDIR /usr/src/app/discordbot/


## PATH="/root/.local/bin:$PATH"


ENV PATH=" ${PATH}:/root/.local/bin" 



RUN curl -sSL https://install.python-poetry.org | python3 - && poetry config virtualenvs.create false && poetry install 


WORKDIR /

COPY . /usr/src/app/discordbot/


ENTRYPOINT [ "python3", "/usr/src/app/discordbot/Discord/circombot.py" ]