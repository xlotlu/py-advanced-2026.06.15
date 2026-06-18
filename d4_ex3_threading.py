from threading import Thread
import time

def sleepy(num, duration=2):
    print(f"» [{num}] gone to sleep")
    time.sleep(duration)
    print(f"» [{num}] waking up")

threads = []
for x in range(5):
    threads.append(
      Thread(target=sleepy, args=(x,), kwargs={'duration': x * 2})
    )
for t in threads:
    # now they be running
    t.start()

for t in threads:
    # must wait for them to be done
    t.join()


# task:
# dat fiind aceste url-uri
URLS = [
   f"https://jsonplaceholder.typicode.com/albums/{num}"
   for num in range(1, 11)
]

# populați o listă cu fiecare din structurile de date
# disponibile în endpoint

import requests
from queue import Queue

threads = []
resp_queue = Queue(maxsize=len(URLS))
results = []

def fetch(url, q):
    response = requests.get(url)
    q.put((url, response.json()))

for url in URLS:
    t = Thread(target=fetch, args=(url, resp_queue))
    threads.append(t)

for t in threads:
    t.start()

# pattern 1:
# ne menținem singuri counter-ul de elemente din queue
#for x in range(len(URLS)):
#    result = responses.get()
#    #responses.task_done()

# pattern 2:
# inițializăm queue-ul cu maxsize, și apoi:

def result_processor(q):
    while True:
        item = q.get()
        try:
            print("» processing", item)
        finally:
            q.task_done()

processor = Thread(target=result_processor, args=(resp_queue,), daemon=True)
processor.start()

for t in threads:
    t.join()
resp_queue.join()
#processor.join()