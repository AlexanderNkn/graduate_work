FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["postgres_elastic_etl/requirements.txt", "postgres_elastic_etl/postgres_elastic_waiter.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/postgres_elastic_waiter.sh

ENTRYPOINT ["/usr/src/code/postgres_elastic_waiter.sh"]

COPY ["postgres_elastic_etl", "./postgres_elastic_etl"]

CMD ["python3", "postgres_elastic_etl/etl_process.py"]