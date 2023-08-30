FROM python:3.11
RUN mkdir -p /usr/src/app/bacalau/

COPY pyproject.toml /usr/src/app/bacalau/pyproject.toml

WORKDIR /usr/src/app/bacalau/
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry config virtualenvs.create false && poetry install 

WORKDIR /
COPY . ./usr/src/app/bacalhau/

ENTRYPOINT ["python3", "/usr/src/app/bacalhau/bacalau_script.py"]
