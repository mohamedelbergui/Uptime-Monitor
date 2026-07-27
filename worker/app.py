import requests
import asyncio


async def check(url:str, freq:int):
    while True:
        response=await asyncio.to_thread(requests.get,url)
        print(f"Code for {url} :", response.status_code)
        await asyncio.sleep(freq)


async def main():
    urls=["https://google.com","https://w3schools.com/python/demopage.htm","https://facebook.com"]
    await asyncio.gather(
    *(check(url,30) for url in urls)
)


asyncio.run(main())