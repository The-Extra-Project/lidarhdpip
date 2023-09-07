FROM python:3.11 as build
RUN mkdir -p /usr/src/app/bacalau/
COPY pyproject.toml /usr/src/app/bacalau/pyproject.toml 

WORKDIR /usr/src/app/bacalau/
RUN curl -sSL https://install.python-poetry.org | python3 - && /root/.local/bin/poetry config virtualenvs.create false 

RUN PATH="/root/.local/bin:$PATH" && poetry --version

RUN  /root/.local/bin/poetry install

FROM build as test

COPY --from=build /usr/src/app/bacalau /usr/src/app/bacalau

WORKDIR /
COPY . ./usr/src/app/bacalhau/

ENTRYPOINT ["python3", "/usr/src/app/bacalhau/bacalau_script.py"]