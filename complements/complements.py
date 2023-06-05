# TODO: Add support for fixed point numbers, e.g. -2.01
#       Possible by left shift (2^x), converting and readding the point.

def dec_to_bv(raw_val: int, required_bytes: int = 0) -> str:
    if raw_val < 0:
        bv_val = '1' + bin(raw_val)[3:]
    else:
        bv_val = '0' + bin(raw_val)[2:]
    if required_bytes == 0:
        return bv_val
    elif (required_bytes - len(bv_val)) > 0:
        return bv_val[0] + (required_bytes - len(bv_val)) * '0' + bv_val[1:]
    else:
        print("[ERROR] required bytes cannot be fulfilled!")
        return bv_val


def dec_to_ones(raw_val: int, required_bytes: int = 0) -> str:
    if raw_val < 0:
        bv_val = dec_to_bv(raw_val, required_bytes)
    else:
        return dec_to_bv(raw_val, required_bytes)

    one_val = bv_val[0]
    for c in bv_val[1:]:
        if c == '1':
            one_val += '0'
        else:
            one_val += '1'

    return one_val


def dec_to_twos(raw_val: int, required_bytes: int = 0) -> str:
    if raw_val < 0:
        bv_val = dec_to_bv(raw_val, required_bytes)
    else:
        return dec_to_bv(raw_val, required_bytes)

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


def print_all_variants(number: int, required_bytes: int = 0) -> None:
    print(f"Number: {number}")
    print(f"BV: {dec_to_bv(number, required_bytes)}")
    print(f"Ones: {dec_to_ones(number, required_bytes)}")
    print(f"Twos: {dec_to_twos(number, required_bytes)}")
    print(" ")


if __name__ == "__main__":
    # print_all_variants(2342)
    # print_all_variants(-49101)
    # print_all_variants(-16)
    # print_all_variants(173)

    # Übungsblatt 04
    # print(f"-1.0 -> {dec_to_twos(-100)}")
    # print(f"2.25 -> {dec_to_twos(225)}")
    # three = int("-2", 16)
    # print(f"{three} -> {dec_to_twos(three)}")

    print(dec_to_bv(-16))
    print(dec_to_ones(-16))
    print(dec_to_twos(-16))
    print(dec_to_bv(-16, 8))
    print(dec_to_ones(-16, 8))
    print(dec_to_twos(-16, 8))