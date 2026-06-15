# creați o funcție ce primind un iterabil
# conținând numere întregi
# returnează o listă nouă
# cu pătratele numerelor

def squares(iter):
    # Pattern de acumulare:
    # 1. instanțiem obiectul final
    new_list = []
    # 2. iterăm prin sursă
    for elem in iter:
        # 3. calculăm valoarea nouă
        v = elem ** 2
        # 4. acumulăm
        new_list.append(v)

    # 5. returnăm obiectul construit
    return new_list

# același exercițiu ca mai sus,
# dar lista nouă conține doar patratele numerelor impare
def odd_squares(iter):
    # Pattern de acumulare cu filtrare:
    # (opțional) 0. adaptăm sursa de date la nevoile curente
    # 1. instanțiem obiectul final
    new_list = []
    # 2. iterăm prin sursă
    for elem in iter:
        # 3. filtrăm
        if elem % 2 == 0:
            # dacă este par nu ne trebuie
            continue

        # 4. calculăm valoarea nouă
        v = elem ** 2
        # 5. acumulăm
        new_list.append(v)

    # 6. returnăm obiectul construit
    return new_list

it = range(5)
# list comprehension !!!
[elem ** 2 for elem in it]

[elem ** 2 for elem in it if elem % 2 == 1]

# set comprehension:
{elem ** 2 for elem in [1, 2, 3, 4, 8, 2, 2]}

# dict comprehension
{elem: elem ** 2 for elem in [1, 2, 3, 4, 8, 2, 2]}

{
    elem: elem ** 2
    for elem in [1, 2, 3, 4, 8, 2, 2]
    if elem % 2
}

# generator expression !!
(elem ** 2 for elem in it if elem % 2 == 1)


# refaceți exercițiul
# IterItemStartsWith / generator_item_startswith
# folosind un generator expression

def generator_item_startswith(source, substr):
    for line in source:
        if line.startswith(substr):
            yield line

def generator_item_startswith(source, substr):
    return (
        line for line in source
        if line.startswith(substr)
    )

with open("concepts_and_cheatsheet.md") as fp:
    for elem in generator_item_startswith(fp, "##"):
        print(elem)

