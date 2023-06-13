def carry_ripple(inp: str, add: str) -> str:
    """ Implements a Carry-Ripple Adder """
    c = False
    inp, add = inp[::-1], add[::-1]
    out = ""
    if len(inp) == len(add):
        for i in range(len(inp)):
            s, c = full_adder(bool(int(inp[i])), bool(int(add[i])), c)
            out = str(int(s)) + out
        out = str(int(c)) + out
    return out


def full_adder(a: bool, b: bool, c: bool) -> tuple(bool, bool):
    """ Implements a full adder """
    ha1, ha2 = half_adder(a, b)
    fa1, fa2 = half_adder(ha1, c)
    return (fa1, (fa2 or ha2))


def half_adder(a: bool, b: bool) -> tuple(bool, bool):
    """ Implements a half adder """
    return ((a ^ b), (a and b))


def test_carry_ripple() -> None:
    """ Provides a unit test for carry_ripple() """
    assert carry_ripple("1", "1") == "10"
    assert carry_ripple("100000", "000001") == "0100001"


if __name__ == "__main__":
    a = carry_ripple("1011", "0110")
    print(a)
