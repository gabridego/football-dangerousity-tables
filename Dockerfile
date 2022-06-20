FROM python:latest

WORKDIR usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY data/calendar.json data/

ENTRYPOINT [ "python", "./main.py" ]