FROM python:3.10.0-slim-buster

ENV POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /morder_gates

COPY poetry.lock pyproject.toml /morder_gates/

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./app /morder_gates/app

ENTRYPOINT ["python"]
CMD ["app/bot.py"]
