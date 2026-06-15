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


# refaceți exercițiul IterItemStartsWith
# folosind o funcție generator

def generator_item_startswith(source, substr):
    for line in source:
        if line.startswith(substr):
            yield line

# with open("concepts_and_cheatsheet.md") as fp:
#     for elem in generator_item_startswith(fp, "##"):
#         print(elem)
