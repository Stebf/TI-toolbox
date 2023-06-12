""" quine.py
    Currently WIP, planned to be a implementation of
    Quine-McCluskey Prime implicants function
"""


def quine(minterm: set[str], dimension: int):
    storeA = dict()
    for monoom in minterm:
        len = monoom.count('1')
        if len in storeA.keys():
            storeA[len] += [monoom]
        else:
            storeA[len] = [monoom]

    print(storeA)


if __name__ == "__main__":
    quine({'0000', '0010', '0011', '1100'}, 1)