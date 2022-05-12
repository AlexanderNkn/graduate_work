FROM python:3.10-slim-bullseye

WORKDIR /usr/src/code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ["movies_admin/requirements.txt", "movies_admin/entrypoint.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/entrypoint.sh

ENTRYPOINT ["/usr/src/code/entrypoint.sh"]

COPY ["movies_admin", "./"]

CMD [ "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
