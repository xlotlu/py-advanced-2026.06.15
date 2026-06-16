# Exercițiu:
# 
# scrieți o funcție

def cp(source, target, overwrite=False, chunksize=8192):
    mode = "wb" if overwrite else "xb"
    with open(source, "rb") as fin, open(target, mode) as fout:
        while contents := fin.read(chunksize):
            fout.write(contents)

# ce, primind căile către fișierele `source` și `target`
# copiază conținutul din `source` în `target`
#
# în cel mai eficient mod,
# fiind capabilă să trateze cu fișiere binare.


# idee, Exercițiu:
# upload de fișiere, chunking, continue on fail

# GPT zice: (netestat)

import os
import requests

CHUNK_SIZE = 1024 * 1024  # 1 MB

def upload_file(path, url, uploaded_bytes=0):
    file_size = os.path.getsize(path)

    with open(path, "rb") as f:
        f.seek(uploaded_bytes)

        while uploaded_bytes < file_size:
            chunk = f.read(CHUNK_SIZE)

            start = uploaded_bytes
            end = start + len(chunk) - 1

            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}"
            }

            response = requests.put(
                url,
                data=chunk,
                headers=headers,
                timeout=30,
            )

            response.raise_for_status()

            uploaded_bytes += len(chunk)

            print(f"Uploaded {uploaded_bytes}/{file_size}")

            # Persist this somewhere (db, file, etc.)
            save_progress(uploaded_bytes)

    return uploaded_bytes


def save_progress(offset):
    with open("upload.progress", "w") as f:
        f.write(str(offset))


def load_progress():
    try:
        with open("upload.progress") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


offset = load_progress()

# try:
#     upload_file("large_file.bin", "https://example.com/upload", offset)
# except Exception as e:
#     print("Upload interrupted:", e)

class ProgressFile:
    def __init__(self, path, start=0):
        self.f = open(path, "rb")
        self.f.seek(start)
        self.sent = start

    def read(self, size=-1):
        data = self.f.read(size)
        self.sent += len(data)
        return data

    def tell_uploaded(self):
        return self.sent

    def close(self):
        self.f.close()

