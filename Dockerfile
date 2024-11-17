FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./notes_sync /app/notes_sync
COPY ./.env /app/.env

CMD ["python3", "-m", "notes_sync"]