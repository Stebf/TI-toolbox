import argparse


def remove_comments(lines: list[str]) -> list[str]:
    """ Removes comments from codelines """
    res: list[str] = []
    for line in lines:
        if '#' in line:
            res += [line[:line.index('#')]]
        elif '//' in line:
            res += [line[:line.index('//')]]
        elif ';' in line:
            res += [line[:line.index(';')]]
        else:
            res += [line]
    return res


def init_storage(preset: dict = {}) -> dict[int, int]:
    """ Helper function to set up storage dict """
    # print(f"[DEBUG] {preset}")
    if preset == {}:
        return {}
    else:
        return preset


def parse_equation_string(equation_str: str) -> dict[int, int]:
    """ Parses a storage preset in line 1 into a dict
        -> Example S(40)=2, S(41)=4
        """
    equation_str = equation_str[:-1]
    pairs = equation_str.split(', ')
    result = {}
    for pair in pairs:
        x_y_str = pair[2:]
        x, y = x_y_str.split(')=')
        x = int(x)
        y = int(y)
        if ',' not in equation_str:
            return {x: y}
        result.update({x: y})
    return result


def show_end(PC: int, ACC, IN1, IN2, S: dict) -> None:
    """ Shows the final results, should be called at the end. """
    print(f'''
    PC:     {PC}
    ACC:    {ACC}
    IN1:    {IN1}
    IN2:    {IN2}

    S(i):   {S}
    ''')


def reti_interpreter(filename: str) -> None:
    """ Interprets reti commands given in a file """
    pc: int = 1
    acc: int = 0
    in1: int = 0
    in2: int = 0

    try:
        with open(filename, 'r') as file:
            lines = remove_comments(file.readlines())

            # Initialize storage array, either with preset or empty
            if lines[0].startswith('S('):
                storage = init_storage(parse_equation_string(lines[0]))
                lines = lines[1:]
            else:
                storage = init_storage()

            while (pc < len(lines)):
                # print(f"[DEBUG] PC: {pc} - {acc}")
                current_line = lines[pc]
                split_line = current_line.split(' ')
                command = split_line[0]
                if 'STOREIN' in current_line:
                    var = split_line[1]
                    if '1' in command:
                        storage[in1 + int(var)] = acc
                    elif '2' in command:
                        storage[in2 + int(var)] = acc
                    pc += 1
                elif 'STORE' in current_line:
                    var = split_line[1]
                    storage[int(var)] = acc
                    pc += 1
                elif 'LOAD' in current_line:
                    var = split_line[1]
                    if var is None:
                        raise KeyError
                    else:
                        var = int(var)
                    if 'LOADIN' in command:
                        if '1' in command:
                            acc = storage[in1 + var]
                        elif '2' in command:
                            acc = storage[in2 + var]
                    elif 'LOADI' in command:
                        acc = var
                    else:
                        acc = storage[var]
                    pc += 1
                elif 'MOVE' in current_line:
                    source = split_line[1]
                    destination = split_line[2]
                    # TODO: Implement Move function
                    if destination != 'PC':
                        pc += 1
                elif 'ADD' in current_line:
                    acc = acc + int(split_line[1])
                    pc += 1
                elif 'SUB' in current_line:
                    acc = acc - int(split_line[1])
                    pc += 1
                elif 'JUMP' in current_line:
                    condition = current_line[4]
                    if condition == ' ':
                        if split_line[1] == '0':
                            # Endless loop on itself -> program ended
                            show_end(pc, acc, in1, in2, storage)
                            return
                        else:
                            # Unconditional jump
                            pc += int(split_line[1])
                    else:
                        # Conditional jump
                        if condition == '=':
                            condition = '=='
                        if eval(str(acc) + ' ' + condition + ' 0'):
                            pc += int(split_line[1])
                        else:
                            pc += 1
                elif 'NOP' in current_line:
                    pc += 1
                else:
                    print(f"[WARN] Unknown command at PC={pc}, skipping this command")
                    pc += 1
            show_end(pc, acc, in1, in2, storage)

    except FileNotFoundError as e:
        print("[ERROR] Coudn't find file.")
        print(f"FileNotFoundError {e}")

    except IOError as e:
        print("[ERROR] Error while reading the file.")
        print(f"IOError {e}")

    except KeyError as e:
        print("[ERROR] Key not found in storage, did you store something in this cell before loading?")
        print(f"KeyError {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to reti code file", type=str)
    args = parser.parse_args()
    if not args.path:
        path = "./code/ggt.reti"
        reti_interpreter(path)
    else:
        reti_interpreter(args.path)