import requests
import asyncio
from datetime import datetime
import psycopg

import os
from dotenv import load_dotenv

load_dotenv("../web/.env")


username=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
db_name=os.getenv("POSTGRES_DB")


# Dictionary tracking currently running monitoring tasks: {service_id: asyncio.Task}
running_tasks = {}

CONN_STRING = f"postgresql://{username}:{password}@localhost:5432/{db_name}"




async def get_services(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM services WHERE services.is_active;")
        return await cursor.fetchall()

async def save_in_db(
        connection,
        id_service:int,
        status_code:int, 
        response_time_ms:float, 
        timestamp: datetime,
        message:str=None
        ):
    try:
        async with  connection.cursor() as cursor:
            query = """
                    INSERT INTO check_results (id_service, status_code, response_time_ms, message, timestamp)
                    VALUES (%s, %s, %s, %s, %s);
                    """
            values = (id_service, status_code, response_time_ms, message, timestamp)
            await cursor.execute(query, values)
            await connection.commit()
            print("save done!")
    except Exception as e:
        if connection:
            connection.rollback()
        print(str(e))


async def check_loop(service):
    """One service = one independent infinite loop, but this task can be cancelled from outside."""
    service_id, name, url, _, interval = service[0], service[1], service[2], service[3], service[4]

    async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn:
        while True:
            try:
                response = await asyncio.to_thread(requests.get, url, timeout=10)
                await save_in_db(
                    connection=conn,
                    id_service=service_id,
                    status_code=response.status_code,
                    response_time_ms=response.elapsed.total_seconds() * 1000,
                    timestamp=datetime.now(),
                    message=response.reason
                )
            except Exception as e:
                print(f"Error checking service {service_id}: {e}")

            await asyncio.sleep(interval)




async def supervisor(sync_interval: int = 15):
    """Periodically syncs running_tasks with the current state of the `services` table."""
    async with await psycopg.AsyncConnection.connect(CONN_STRING) as conn:
        while True:
            services = await get_services(conn)
            current_ids = {s[0] for s in services}

            # Start tasks for new services
            for service in services:
                service_id = service[0]
                if service_id not in running_tasks:
                    print(f"Starting monitoring for service {service_id}")
                    task = asyncio.create_task(check_loop(service))
                    running_tasks[service_id] = task

            # Cancel tasks for removed services
            for service_id in list(running_tasks.keys()):
                if service_id not in current_ids:
                    print(f"Stopping monitoring for service {service_id} (removed)")
                    running_tasks[service_id].cancel()
                    del running_tasks[service_id]

            await asyncio.sleep(sync_interval)

asyncio.run(supervisor())