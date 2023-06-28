import random
from complements import *
from back_comp import *

""" Provides testing capabilities for the complements module """


def test_bv() -> None:
    for i in range(32):
        n = random.randint(-1023, 1023)
        assert bv_to_dec(dec_to_bv(n)) == n


def test_ones() -> None:
    for i in range(32):
        n = random.randint(-1023, 1023)
        assert ones_to_dec(dec_to_ones(n)) == n


def test_twos() -> None:
    for i in range(32):
        n = random.randint(-1023, 1023)
        assert twos_to_dec(dec_to_twos(n)) == n