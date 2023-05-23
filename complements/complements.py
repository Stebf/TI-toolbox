# TODO: Add support for fixed point numbers, e.g. -2.01
#       Possible by left shift (2^x), converting and readding the point.
# TODO: Add parameter for fixed length, e.g. 8 bit

def dec_to_bv(raw_val: int) -> str:
    if raw_val < 0:
        bv_val = '1' + bin(raw_val)[3:]
    else:
        bv_val = '0' + bin(raw_val)[2:]
    return bv_val


def dec_to_ones(raw_val: int) -> str:
    if raw_val < 0:
        bv_val = '1' + bin(raw_val)[3:]
    else:
        bv_val = '0' + bin(raw_val)[2:]
        return bv_val

    one_val = bv_val[0]
    for c in bv_val[1:]:
        if c == '1':
            one_val += '0'
        else:
            one_val += '1'

    return one_val


def dec_to_twos(raw_val: int) -> str:
    if raw_val < 0:
        bv_val = '1' + bin(raw_val)[3:]
    else:
        bv_val = '0' + bin(raw_val)[2:]
        return bv_val

    one_val = bv_val[0]
    for c in bv_val[1:]:
        if c == '1':
            one_val += '0'
        else:
            one_val += '1'

    two_val = ''
    done = False
    for d in one_val[::-1]:
        if d == '0' and not done:
            two_val += '1'
            done = True
        elif d == '1' and not done:
            two_val += '0'
        else:
            two_val += d

    two_val = two_val[::-1]

    return two_val


def print_all_variants(number: int) -> None:
    print(f"Number: {number}")
    print(f"BV: {dec_to_bv(number)}")
    print(f"Ones: {dec_to_ones(number)}")
    print(f"Twos: {dec_to_twos(number)}")
    print(" ")


if __name__ == "__main__":
    # print_all_variants(2342)
    # print_all_variants(-49101)
    # print_all_variants(-16)
    # print_all_variants(173)

    # Übungsblatt 04
    print(f"-1.0 -> {dec_to_twos(-100)}")
    print(f"2.25 -> {dec_to_twos(225)}")
    three = int("-2", 16)
    print(f"{three} -> {dec_to_twos(three)}")