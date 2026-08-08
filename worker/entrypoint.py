import psycopg
import time
import os
from dotenv import load_dotenv

load_dotenv()


host = os.getenv("POSTGRES_HOST")
username=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
db_name=os.getenv("POSTGRES_DB")

while True:
    try:
        CONN_STRING = f"postgresql://{username}:{password}@{host}:5432/{db_name}"
        conn = psycopg.connect(CONN_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM services")
        break
    except:
        print("wait for the database")
        time.sleep(3)