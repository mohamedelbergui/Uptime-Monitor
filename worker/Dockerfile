FROM python:3.13-slim


WORKDIR /worker

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


CMD python entrypoint.py && python app.py