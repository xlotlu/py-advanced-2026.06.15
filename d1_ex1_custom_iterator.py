# scrieți un iterator
class FileLineStartsWith:
    def __init__(self, filename, substr):
        pass # statement no-op

# care, atunci când este iterat
# returnează liniile de text din `filename`
# care încep cu `substr`


class FileLineStartsWith:
    def __init__(self, filename, substr):
        self.filename = filename
        self.substr = substr

        self._fp = open(filename)

    def __next__(self):
        # ne bazăm pe faptul că `self._fp`
        # are un pointer intern,
        # deci `for` rulat de la un __next__
        # la altul continuă de unde a rămas
        for line in self._fp:
            if line.startswith(self.substr):
                return line

        raise StopIteration()

    def __iter__(self):
        return self


# același exercițiu, dar pentru elementele
# dintr-o listă

class LstItemStartsWith:
    def __init__(self, lst, substr):
        self.lst = lst
        self.substr = substr

        self._source_iter = iter(lst)

    def __iter__(self):
        return self

    def __next__(self):
        for line in self._source_iter:
            if line.startswith(self.substr):
                return line

        raise StopIteration()

# putem să facem un iterator general-purpose
# ce merge cu orice datatype de input?
# (cu condiția să fie iterabil?)

class IterItemStartsWith:
    def __init__(self, source, substr):
        self.source = source
        self.substr = substr

        # we create an internal iterator,
        # so that we can iterate over it repeatedly
        # and make sure it is consumed only once.
        self._source_iter = iter(source)

    def __iter__(self):
        return self

    def __next__(self):
        # we will iterate through the internal iterator.
        # it may seem strange, but it is all right
        # cause it only gets consumed once!
        for line in self._source_iter:
            if line.startswith(self.substr):
                return line

        raise StopIteration()


# usage:

mylst = ["txt 1", "## comentariu 1", "txt 2", "## comentariu 2" ]

for elem in IterItemStartsWith(mylst, "##"):
    print(elem)

with open("concepts_and_cheatsheet.md") as fp:
    for elem in IterItemStartsWith(fp, "##"):
        print(elem)


# implementare alternativă
# (nepreferată în acest caz particular)

class LstItemStartsWith:
    def __init__(self, lst, substr):
        self.lst = lst
        self.substr = substr

        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        for idx in range(self._current_index, len(self.lst)):
            elem = self.lst[idx]
            self._current_index += 1

            if elem.startswith(self.substr):
                return elem

        raise StopIteration()

###
# loc de parcat cursorul
#
###