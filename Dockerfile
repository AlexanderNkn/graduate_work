FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY requirements.txt .

RUN apt update && apt install -y netcat gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* 

COPY entrypoint.sh .

RUN chmod +x /usr/src/code/entrypoint.sh

ENTRYPOINT ["/usr/src/code/entrypoint.sh"]

COPY ./src .

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
