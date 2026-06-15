# scriem o funcție generator ce ne dă pătratele numerelor din iterabilul de input
def squares(it):
    for elem in it:
        yield elem ** 2
# for x in squares(range(5)):
#     print(x)
# for x in squares((17, 12, 5, 8)):
#     print(x)


# scrieți o funcție generator ce produce pătratele numerelor impare
# din iterabilul de input
def odd_squares(it):
    for elem in it:
        if elem % 2 == 1:
            yield elem ** 2
        