FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["assistant_api/requirements.txt", "./"]

RUN apt update && apt install -y gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY ["assistant_api", "./assistant_api"]

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "assistant_api.src.main:app", "--bind", "0.0.0.0:8000"]
