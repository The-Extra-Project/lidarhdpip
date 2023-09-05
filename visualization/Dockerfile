FROM --platform=linux/amd64 python:3.8 as build

RUN mkdir -p /usr/src/app/visualization

COPY pyproject.toml /usr/src/app/visualization/pyproject.toml

WORKDIR /usr/src/app/visualization   

ENV PATH = "${PATH}:/root/.local/bin"


RUN curl -sSL https://install.python-poetry.org | python3 -  && poetry install





FROM python:3.8

RUN mkdir -p /usr/src/app/visualization

COPY --from=build /usr/src/app/visualization /usr/src/app/visualization

WORKDIR /

RUN poetry config virtualenvs.create false

COPY . /usr/src/app/visualization


EXPOSE 8053

CMD ["streamlit run ", "app.py"]