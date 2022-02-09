FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["../../auth", "./"]

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* 

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "app:asgi_app", "--bind", "0.0.0.0:5000"]