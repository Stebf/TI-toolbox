import argparse


def bv_to_dec(raw_val: str) -> int:
    """ Converts binary number with sign bit to decimal """
    sign = raw_val[0]
    number = int(raw_val[1:], 2)

    if sign == '1':
        return -1 * number
    else:
        return number


def ones_to_dec(raw_val: str) -> int:
    """ Converts one's complement binary number to decimal """
    bv = bv_to_dec(raw_val)
    if bv < 0:
        bv_val = ""
        for c in raw_val:
            if c == '1':
                bv_val += '0'
            else:
                bv_val += '1'
        return -1 * bv_to_dec(bv_val)
    else:
        return bv


def twos_to_dec(raw_val: str) -> int:
    """ Converts two's complement binary number to decimal """
    bv = bv_to_dec(raw_val)
    if bv < 0:
        return ones_to_dec(raw_val) - 1
    else:
        return bv


def check_binary(raw_val: str) -> None:
    """ Raises an ValueError if a char in the provided str is not 0 or 1 """
    for c in raw_val:
        if c not in ["1", "0"]:
            raise ValueError("Please provide a binary number as str.")


def show_all_variants(raw_val: str) -> None:
    """ Prints out all three variants """
    print(bv_to_dec(raw_val))
    print(ones_to_dec(raw_val))
    print(twos_to_dec(raw_val))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "-number", help="The binary you want to convert", type=str)
    parser.add_argument("-k", "-kind", help="The kind of complement it is", type=str)
    args = parser.parse_args()
    check_binary(args.n)
    match args.k:
        case "0":
            print(bv_to_dec(args.n))
        case "1":
            print(ones_to_dec(args.n))
        case "2":
            print(twos_to_dec(args.n))
        case _:
            show_all_variants(args.n)