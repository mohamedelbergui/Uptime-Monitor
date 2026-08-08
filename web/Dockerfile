FROM python:3.13-slim

WORKDIR /Uptime_Monitor
COPY requirements.txt .

RUN pip install -r requirements.txt && pip install gunicorn

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]