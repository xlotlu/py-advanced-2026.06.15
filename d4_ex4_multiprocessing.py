from multiprocessing import Process, current_process
import requests


URLS = [
   f"https://jsonplaceholder.typicode.com/albums/{num}"
   for num in range(1, 11)
]

procs = []

import random
from time import sleep

def fetch(url):
    response = requests.get(url)
    sleep(random.randint(1, 20))
    print("» processed", url, response.json())

def main():
    for url in URLS:
        p = Process(target=fetch, args=(url, ))
        procs.append(p)

    for p in procs:
        p.start()

    for p in procs:
        p.join()


print("de 2 ori", current_process())

if __name__ == "__main__":
    main()
