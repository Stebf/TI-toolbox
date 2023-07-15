def decompile_one(command: str) -> str:
    command = sanitize(command)
    command_type = command[0:2]
    specification = command[2:8]
    parameter = command[8:]
    assert command_type + specification + parameter == command, 'Splitting of command failed.'

    registers = {'00': 'PC ', '01': 'IN1 ', '10': 'IN2 ', '11': 'ACC '}

    match command_type:
        case '01':
            modi = {'00': 'LOAD ', '01': 'LOADIN1 ', '10': 'LOADIN2 ', '11': 'LOADI '}
            return modi[specification[0:2]] + registers[specification[4:6]] + str(int(parameter, 2))
        case '10':
            if specification[0:2] == '11':
                return 'MOVE ' + registers[specification[2:4]] + registers[specification[4:6]]
            else:
                modi = {'00': 'STORE ', '01': 'STOREIN1 ', '10': 'STOREIN2 '}
                return modi[specification[0:2]] + str(int(parameter, 2))
        case '00':
            modi = {'010': 'SUB', '011': 'ADD', '100': 'OR', '110': 'AND'}
            immediate = {'0': 'I ', '1': ' '}
            return modi[specification[1:4]] + immediate[specification[0]] + registers[specification[4:6]] + str(int(parameter, 2))
        case '11':
            if specification[0:3] == '000':
                return 'NOP'
            else:
                modi = {'001': '> ', '010': '= ', '011': '>= ', '100': '< ', '101': '!= ', '110': '<= ', '111': ' '}
                return 'JUMP' + modi[specification[0:3]] + str(int(parameter, 2))

    return '[!] Something went wrong'


def decompile_file_to_str(binary_file: str) -> str:
    result = ''
    with open(binary_file, 'r') as file:
        for line in file:
            result += decompile_one(line) + '\n'
    return result


def decompile_file_to_file(binary_file: str, new_path: str) -> None:
    new_file = open(new_path, 'a')
    new_file.write(decompile_file_to_str(binary_file=binary_file))
    new_file.close()


def sanitize(command: str) -> str:
    result = ''.join([bit for bit in command if bit in '01'])
    if len(result) != 32:
        raise ValueError
    return result


def test_decompile_one() -> None:
    assert decompile_one('01 11 11 11 000000000000000000000001') == 'LOADI ACC 1'
    assert decompile_one('11000000000000000000000000000000') == 'NOP'
    assert decompile_one('00001111000000\n000000000000000001') == 'ADDI ACC 1'
    assert decompile_one('10000000000000000000000000000011') == 'STORE 3'


if __name__ == '__main__':
    test_decompile_one()