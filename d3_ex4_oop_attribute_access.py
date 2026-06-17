class MyClass:
    z = 2222
    def __init__(self):
        self.x = 12
        self.y = 15

    def __getattribute__(self, name):
        print("getting attribute", name)
        return super().__getattribute__(name)

    def __getattr__(self, name):
        # îl folosim pentru atribute ce nu există
        if name == "abc":
            return 55
        
        # cel mai probabil dacă am făcut așa ceva
        # în restul cazurilor vrem să
        raise AttributeError()
    
    def __setattr__(self, name, value):
        print("setting attribute", name)
        super().__setattr__(name, value)

            
#o = MyClass()
#o.abc


# Exercițiu
# Scrieți o clasă BankAccount
# cu atributele id, balance, overdraft 
#
# implementați metodele `withdraw()` și `deposit()`
#
# apoi scrieți metoda `__setattr__` astfel încât
# dacă rezultatul final al balance ar depăși -overdraft
# să refuze tranzacția.


class BankAccount:
    def __init__(self, id, balance=0, overdraft=0):
        self.id = id
        self.overdraft = overdraft
        self.balance = balance

    def __repr__(self):
        return f"BankAccount(id={self.id}, balance={self.balance}, overdraft={self.overdraft})"

    def deposit(self, amount):
        self.balance += amount
        #print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        self.balance -= amount

    def __setattr__(self, name, value):
        if name == "balance":
            if value < -self.overdraft:
                raise ValueError("Account balance exceeds overdraft")

        super().__setattr__(name, value)


# replicați pattern-ul folosind @property și setter

class BankAccount:
    def __init__(self, id, balance=0, overdraft=0):
        self.id = id
        self.overdraft = overdraft
        self.__balance = balance

        BankAccountsCollection().append(self)

    def __repr__(self):
        return f"BankAccount(id={self.id}, balance={self.balance}, overdraft={self.overdraft})"

    def deposit(self, amount):
        self.balance += amount
        #print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        self.balance -= amount

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < -self.overdraft:
            raise ValueError("Account balance exceeds overdraft")
        self.__balance = value


# clasă singleton BankAccountsCollection
# ce la crearea unui BankAccount adaugă la sine obiectul creat
# și suportă item access după id-ul contului
# ...
# și să fie și iterabil

class BankAccountsCollection:
    _object = None
    _accounts = {}

    def __new__(cls, *args, **kwargs):
        if cls._object is None:
            cls._object = super().__new__(cls, *args, **kwargs)

        return cls._object

    def __getitem__(self, key):
        return self._accounts[key]

    def __setitem__(self, key, value):
        self._accounts[key] = value

    def append(self, account):
        self[account.id] = account

    def __iter__(self):
        return iter(self._accounts.values())

