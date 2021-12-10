FROM python:3.10-slim-bullseye

WORKDIR /usr/src/code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/*

CMD [ "python3", "postgres_to_es/etl_process.py"]
