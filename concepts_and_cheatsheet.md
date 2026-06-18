# Concepte

lista este mutable

Python este o specificație.
noi lucrăm cu implementarea "CPython"

Jython (Java)
IronPython (C#)
micropython / CircuitPython


în Python _totul_ este un obiect


FIFO pe listă, adică

```python
lst.append()
lst.append()
lst.pop(0)
lst.pop(0)
```

implică reindexarea tuturor elementelor.

la fel și...

```python
lst.insert(0)
```


# Iteratori, iterabile

un iterabil = element ce poate fi iterat.
              adică în limbaj de Python,
              înseamnă că poate fi transformat
              într-un iterator. adică are metoda __iter__()

un iterator = și el un element ce poate fi iterat. deci are __iter__() --> self.
              dar este elementul concret din care se "mănâncă" element cu element.
              deci implementează metoda __next__()

> în spate, iterația se face _întotdeauna_
> pe un iterator


## protocolul de iterare:

- la fiecare trecere prin bucla unui for,
- se face next() pe iteratorul sursă
- dacă este consumat, raise StopIteration


## ca să facem un iterator:

1. clasa implementează metoda __iter__(self),
   ce returnează iteratorul propriu-zise,
2. care operator propriu-zis implementează
   metoda __next__(self)

Atenție: dacă este deja iterator,
mai mult ca sigur vreți ca:

```python
def __iter__(self):
    return self
```

[!!] we use iterators in the first place
ca să nu băgăm totul în memorie de la început


# Pattern-ul de acumulare

0. (opțional) adaptăm sursa de date la nevoile curente
1. instanțiem obiectul final
2. iterăm prin sursă
3. filtrăm
4. calculăm valoarea nouă
5. acumulăm
6. returnăm obiectul construit


# Decoratorul

este:
- o funcție
- ce primește ca parametru o funcție
- și returnează o funcție

iar restul este "syntactic sugar"


# Context managers:

- sunt deschiși cu statementul with
- are custom logic la deschidere și la închidere


# Concurrency vs parallelism

concurrency ⊂ parallelism

în Python:
GIL = global interpreter lock
  --> implicația este: multi-threading în Python
                       = single CPU core!

[pânâ acum, în Python]
True parallelism:
  - multiprocessing (subprocese)
  - you need some way to communicate between them
    (from multiprocessing import shared_memory)

[de curând]
Există python free-threaded


înainte:
  - aplicații I/O-bound: threading
  - aplicații CPU-bound: multiprocessing

acum (cu python free-threaded)
  - threading ok și pentru I/O-bound și pentru CPU-bound


asyncio:
 -- single-process, single-threaded
        ---> potrivit pentru task-urio I/O-bound
 -- extrem de eficient
 -- paradigmă diferită:
      -- unde threading-ul însemna sincronizare de mână
         în fiecare loc unde putea exista contenție pe resursă
      -- cu async doar spunem că noi așteptăm (await)
         să se termine ceva din spate async
         și scheduler-ul este liber să ruleze altă coroutină


# despre Ipython
%load_ext autoreload
%autoreload 2


# essential wisdom

There are 2 really hard problems in programming:
- naming things
- cache invalidation
- off-by-one errors

Never underestimate the bandwith of a station wagon chock full of tapes
hurtling down the highway.

PEBKAC = problem exists between keyboard and chair

"User Error: replace user and press any key"
