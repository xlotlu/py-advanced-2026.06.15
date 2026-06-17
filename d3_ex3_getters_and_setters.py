class MyClass:
    def __init__(self):
        self.__x = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        # condiționale etc.
        self.__x = value

    @x.deleter
    def x(self):
        print("l-am șters pe x....")
        del self.__x

