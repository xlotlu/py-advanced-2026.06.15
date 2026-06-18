import asyncio

"""
async def main():
    print("i be running")
    await asyncio.sleep(2)
    print("i be done")

asyncio.run(main())
"""

"""
# this is blocking!
# from time import sleep

async def t1():
    print("i am t1")
    await asyncio.sleep(2)
    print("t1: done")

async def t2():
    print("i am t2")
    await asyncio.sleep(2)
    print("t2: done")

async def main():
    

asyncio.run(main())
"""


# Exercițiu:
# rescrieți exemplul cu fetch 
# folosind asyncio

import requests


URLS = [
   f"https://jsonplaceholder.typicode.com/albums/{num}"
   for num in range(1, 11)
]

from random import randint

async def fetch(url):
    response = requests.get(url)
    #    blocking ^^
    print("returning for:", url)
    return response.json()


# pattern 1:
#
# folosim gather când
# 1) vrem să menținem ordinea rezultatelor
#    corelată cu input-ul inițial
#
# 2) pentru task-uri main-level
#    (care au fiecare while True al lor)
async def main():
    tasks = [fetch(url) for url in URLS]

    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

#asyncio.run(main())

from httpx import AsyncClient


async def fetch(url, client):
    response = await client.get(url)
    print("returning for:", url)
    return response.json()

# pattern 2:
#
# procesăm după cum sunt gata
# (!!!!! și folosim un library async-ready !!!!!)
async def main():
    async with AsyncClient() as client:
        tasks = [fetch(url, client) for url in URLS]

        for task in asyncio.as_completed(tasks):
            result = await task

            print(result)

asyncio.run(main())
