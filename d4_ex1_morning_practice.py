# scrieți un decorator care loghează call-urile tututor funcțiilor,
# cu semnătura

DEFAULT_LOG_PATH = "/tmp/my-logger.log"

def logthis(path=DEFAULT_LOG_PATH):
    pass

# puteți să îl faceți class-based decorator, cu condiția să
# îi păstrați semnătura.

## usage-ul său va fi
#@logthis()
#def myfunc(arg, kwarg="etc"):
#    pass

## sau 
#@logthis("/path/my.log")
#def myfunc2(arg, kwarg="etc"):
#    pass

## sau 
#@logthis(path="/path/my.log")
#def myfunc3(arg, kwarg="etc"):
#    pass

# însemnând: nu faceți un decorator hibrid.

# asigurați-vă că fiecare fișier cu loguri
# este deschis o singură dată per proces

# fiecare log entry va conține următoarele
# - datetime
# - namespace și numele funcției
# - argumentele pasate
# - result

# ===============================================
from datetime import datetime
from itertools import chain
from d3_ex2_flow_de_instantiere import MultitonMeta


class logthis(metaclass=MultitonMeta):
    LOG_ENTRY = "[{timestamp}] {module}.{name}({args_and_kwargs}) --> {result}"

    def __init__(self, path=DEFAULT_LOG_PATH):
        self.path = path
        self.fp = open(self.path, "a")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # log the call
            self.add_log(func, result, args, kwargs)
            
            # and return
            return result
        return wrapper
    
    def __del__(self):
        self.fp.close()

    def add_log(self, func, result, f_args, f_kwargs):
        _all_args = chain(
            (
                repr(arg)
                for arg in f_args
            ), (
                f'{k}={repr(v)}'
                for k, v in f_kwargs.items()
            )
        )

        message = self.LOG_ENTRY.format(
            timestamp=datetime.now(),
            module=func.__module__,
            name=func.__qualname__,
            args_and_kwargs=', '.join(_all_args),
            result=result
        )
        
        self.fp.write(message + "\n")
        self.fp.flush()


@logthis()
def myfunc(arg, kwarg="etc"):
    return "some " + arg

# sau 
@logthis("/tmp/myfunc2.log")
def myfunc2(arg, num, kwarg="etc"):
    return num * arg

# sau 
@logthis(path="/tmp/func3.log")
def myfunc3(arg, kwarg="etc"):
    return "iar, un.. " + arg
        
f1 = myfunc("etc")
f2 = myfunc2("1", 2, kwarg="etc")
f3 = myfunc3("arg", kwarg="etc")