# cazul cel mai simplu:
# decorăm o funcție fără argumente
def deco(func):
    print("eu sunt decoratorul")
    def _inner():
        print("eu sunt funcția cea nouă")
        return func()
    print("și returnez funcția nouă")
    return _inner

# complexitate crescută:
# pasăm toate argumentele la funcția decorată
def deco(func):
    print("eu sunt decoratorul")
    def _inner(*args, **kwargs):
        print("eu sunt funcția cea nouă")
        return func(*args, **kwargs)
    print("și returnez funcția nouă")
    return _inner

@deco
def myfunc(x, y, kwarg1=None):
    return 52

# complexitatea aproape finală:
# decoratorul nostru primește argumente
# (deci funcție în funcție în funcție)
def decox(filename=None):
    # el returnează o funcție decorator
    def _deco_func(func):
        def _inner(*args, **kwargs):
            print("eu sunt func decorată")
            print("funcția 'reală' apelată", func.__module__, func.__name__)
            print("cu args", args)
            print("cu kwargs", kwargs)
            print("iar decoratorul a fost instanțiat cu", filename)
            return func(*args, **kwargs)
        return _inner
    return _deco_func

@decox("/un/path")
def myfunc(x, y, kwarg1=None):
    return 52



# Exercițiu
# reproduceți exemplul "complexitate crescută"
# folosind class-based decorator

class mydeco:
    def __init__(self, func):
        print("» init deco")
        self.func = func

    def __call__(self, *args, **kwargs):
        print("» call de func")
        return self.func(*args, **kwargs)

@mydeco
def myfunc(x, y):
    return x + y


# Exercițiu
# reproduceți exemplul "complexitate aproape finală"
# folosind class-based decorator

class mydeco:
    def __init__(self, filename):
        print("» init deco class")
        self.filename = filename

    def __call__(self, func):
        print("» initializare deco")

        def _inner(*args, **kwargs):
            print("» mă rulez, eu sunt funcția decorată")
            return func(*args, **kwargs)

        return _inner

@mydeco("/un/path")
def myfunc(x, y):
    return x + y


# complexitate maximă:
# decorator hibrid, cu argument opțional
# ce funcționează cu și fără argumente

class mydeco:
    def __init__(self, *args, path=None):
        self.func = None
        self.path = path
        
        if args:
            if callable(args[0]):
                self.func = args[0]
            else:
                self.path = args[0]
            
        print(self.func, self.path)
        
    def __call__(self, *args, **kwargs):
        if self.func:
            # actual function call
            return self._inner(*args, **kwargs)
        else:
            # make wrapper func
            self.func = args[0]
            return self._inner

    def _inner(self, *args, **kwargs):
        print("» actually running the func")
        return self.func(*args, **kwargs)

@mydeco(path="/un/path")
def myfunc1(x, y):
    return x + y

@mydeco("/alt/path")
def myfunc2(x, y):
    return x + y

@mydeco
def myfunc3(x, y):
    return x + y

# scrieți un decorator care loghează call-urile tututor
# funcțiilor într-un fișier

