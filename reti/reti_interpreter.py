from argparse import ArgumentParser
from decompiler import decompile_one


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


class Command():
    register: dict[str, int] = {}
    storage = {}

    def __init__(self, storage_preset={}) -> None:
        self.register['PC'] = 1
        self.register['ACC'] = 0
        self.register['IN1'] = 0
        self.register['IN2'] = 0
        self.storage: dict[int, int] = storage_preset
        return

    def load(self, modus: str, destination: str, parameter: str):
        match len(modus):
            case 0:
                self.register[destination] = self.storage[int(parameter)]
            case 1:
                self.register[destination] = int(parameter)
            case 3:
                self.register[destination] = self.storage[self.register[modus] + int(parameter)]
        if destination != 'PC':
            self.register['PC'] += 1
        return

    def store(self, modus: str, parameter: str):
        if modus == '':
            self.storage[int(parameter)] = self.register['ACC']
        else:
            self.storage[self.register[modus] + int(parameter)] = self.register['ACC']
        self.register['PC'] += 1
        return

    def move(self, source: str, destination: str):
        self.register[destination] = self.register[source]
        if destination != 'PC':
            self.register['PC'] += 1
        return

    def compute(self, command: str, destination: str, parameter: str):
        param: int
        if command.endswith('I'):
            param = int(parameter)
            command = command[:-1]
        else:
            param = self.storage[int(parameter)]

        match command:
            case 'SUB':
                self.register[destination] = self.register[destination] - param
            case 'ADD':
                self.register[destination] = self.register[destination] + param

            # TODO: logic functions not yet implemented, binary representations needed.
            case 'OPLUS':
                raise NotImplementedError
            case 'OR':
                raise NotImplementedError
            case 'AND':
                raise NotImplementedError

        if destination != 'PC':
            self.register['PC'] += 1
        return

    def nop(self) -> None:
        self.register['PC'] += 1
        return

    def jump(self, modus, parameter):
        if modus == '=':
            modus = '=='
        if modus == '':
            if parameter == '0':
                self.print_status()
                return
            self.register['PC'] += int(parameter)
            return
        if eval(str(self.register['ACC']) + ' ' + modus + ' 0'):
            self.register['PC'] += int(parameter)
        else:
            self.register['PC'] += 1

    def print_status(self) -> None:
        print(self.register)
        print(self.storage)
        return


def reti_interpreter(filename: str, type: str = 'reti') -> None:
    """ Interprets reti commands given in a file """

    try:
        with open(filename, 'r') as file:
            lines = remove_comments(file.readlines())

        if lines[0].startswith('S('):
            cmd = Command(parse_equation_string(lines[0]))
            lines = lines[0:]
        else:
            cmd = Command()

        while (cmd.register['PC'] < len(lines)):
            # cmd.print_status()
            if type == 'binary':
                current_line = decompile_one(lines[cmd.register['PC']].strip('\n'))
            else:
                current_line = lines[cmd.register['PC']].strip('\n')
            split_line = current_line.split(' ')
            command = split_line[0]
            if command.startswith('LOAD'):
                if type == 'simple':
                    dest = 'ACC'
                else:
                    dest = split_line[1]
                cmd.load(command[4:], dest, split_line[-1])
            elif command.startswith('STORE'):
                cmd.store(command[5:], split_line[1])
            elif command.startswith('MOVE'):
                cmd.move(split_line[1], split_line[2])
            elif command.startswith('NOP'):
                cmd.nop()
            elif command.startswith('JUMP'):
                cmd.jump(command[4:], split_line[1])
            else:
                if type == 'simple':
                    dest = 'ACC'
                else:
                    dest = split_line[1]
                cmd.compute(command, dest, split_line[-1])

        cmd.print_status()

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
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", help="path to reti code file", type=str)
    parser.add_argument("-t", "--type", help="type of the given file", type=str, choices=['reti', 'simple', 'binary'])
    args = parser.parse_args()
    if not args.path:
        path = "./code/ggt-v2.reti"
        reti_interpreter(path, 'reti')
    else:
        reti_interpreter(args.path, args.type)