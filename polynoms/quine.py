""" quine.py
    Currently WIP, planned to be a implementation of
    Quine-McCluskey Prime implicants function
"""


def quine(minterm: str, dimension: int):
    logic = []
    logic[0] = minterm
    i = 0
    primes = {}

    while logic != [] and i < dimension:
        logic[i + 1]