FROM python:3.13.14-slim-trixie

WORKDIR /Uptime_Monitor
COPY requirements.txt .

RUN pip install -r requirements.txt && pip install gunicorn

COPY . .

CMD ["gunicorn","-w","4","-b","0.0.0.0:8000","run:app"]