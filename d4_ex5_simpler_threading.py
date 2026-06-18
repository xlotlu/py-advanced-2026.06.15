from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests


URLS = [
   f"https://jsonplaceholder.typicode.com/albums/{num}"
   for num in range(1, 11)
]


def fetch(url):
    response = requests.get(url)
    return response.json()


def do_thread_pool():
    with ThreadPoolExecutor() as ex:
        for url, result in zip(URLS, ex.map(fetch, URLS)):
            print(url, result)

def do_process_pool():
    # same pattern, but....
    # !!!WARNING!!!
    # this must be used under a function,
    # which 
    # or it goes BOOM!
    with ProcessPoolExecutor() as ex:
        for url, result in zip(URLS, ex.map(fetch, URLS)):
            print(url, result)

from datetime import datetime
# ATENȚIE (continuarea acelui WARNING de mai sus)
# când lucrăm cu ProcessPoolExecutor
# codul main-level se execută și în alt sub-proces:
print("cineva mă rulează!!", datetime.now())

# deci vrem ca totul să fie self-contained
# în funcții, și în main-level entry-point conditional:

if __name__ == '__main__':
    print("=== threads ===")
    do_thread_pool()

    print("=== processes ===")
    do_process_pool()