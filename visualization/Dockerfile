FROM python:3.8

RUN mkdir -p /usr/src/app/visualization
COPY pyproject.toml /usr/src/app/pyproject.toml
WORKDIR /usr/src/app   

ENV PATH = "${PATH}:/root/.local/bin"

RUN curl -sSL https://install.python-poetry.org | python3 - &&  poetry install

WORKDIR /

RUN poetry config virtualenvs.create false

COPY . /usr/src/app/visualization


EXPOSE 8053

CMD ["streamlit run ", "app.py"]