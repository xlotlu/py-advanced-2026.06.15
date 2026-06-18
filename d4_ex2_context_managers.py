# open(path, encoding="utf-8")
class MyContextManager:
    def __init__(self, path, encoding="utf-8"):
        print("inițializat")
        pass

    def __enter__(self):
        print("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exiting")
        print(exc_type, exc_val, exc_tb)
        pass


class CtxThing:
    def __enter__(self):
        return something

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def ctx_builder(args):
    return CtxThing()


#with MyContextManager("/path") as myvar:
#    #1 / 0
#    pass

# Exercițiu:
# scrieți un context manager care deschide șî închide
# o bază de date sqlite

import sqlite3

class SQLiteContextManager:
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        
    def __enter__(self):
        return self.conn
        
    def __exit__(self, exc_type, exc, tb):
        self.conn.close()


with SQLiteContextManager("/tmp/my.db") as db:
    cur = db.cursor()
    print(cur)

# hacky (but simple) way to implement a context manager
from contextlib import contextmanager

@contextmanager
def sqlite_manager(dbfile):
    # set-up
    conn = sqlite3.connect(dbfile)

    # one-time yield, ce ar returna __enter__
    yield conn 

    # cleanup, __exit__ phase
    conn.close()  # tear-down

with sqlite_manager("/tmp/another.db") as conn:
    cur = conn.cursor()
    result = cur.execute("SELECT 1")
    print(result.fetchall())


# the simplest way to the the above, use contextlib.closing:
from contextlib import closing

with closing(sqlite3.connect("/tmp/yet-another.db")) as conn:
    cur = conn.cursor()
    result = cur.execute("SELECT 2")
    print(result.fetchall())

# with closing(sqlite3.connect(dbfile))
# with closing(open("file"))
# with closing(urlopen(url))


# let's redirect all printing (i.e. writing to stdout)
# temporarily to a file

import sys

@contextmanager
def redir_stdout(path):
    with open(path, 'a') as fp:
        _stdout = sys.stdout
        sys.stdout = fp

        yield

        sys.stdout = _stdout

with redir_stdout("/tmp/output.txt"):
    print("chestii")
    print("și povești")


# scrieți un context manager `timeit()`
# care face print la sys.stderr
# cu durata de execuție a blocului interior.
#
### putem să îl facem să poată funcționa și ca decorator?

import sys
from datetime import datetime

class timeit:
    def __init__(self, func=None):
        # if func is none, this is a context manager
        self.func = func

        self.start = datetime.now()

    def _stop(self):
        self.end = datetime.now()
        duration = self.end - self.start
        print(f"Executed time: {duration}", file=sys.stderr)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop()

    def __call__(self, *args, **kwargs):
        retval = self.func(*args, **kwargs)
        self._stop()
        return retval

import time
with timeit():
    print("» inside context")
    time.sleep(.2)

@timeit
def mylongfunc():
    print("» inside func")
    time.sleep(.3)
    return 55

print('executing', mylongfunc())
