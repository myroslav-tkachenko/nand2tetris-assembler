import sys
import os
from parser_module import Parser
from code_module import Code
from predefined_symbols import predefined_symbols


def main():
    input_filename = get_full_input_filename()
    output_filename = get_full_output_filename(input_filename)

    if not input_filename:
        print('You need to specify an input filename.')
        return

    if not os.path.exists(input_filename):
        print('The file {} does not exists.'.format(input_filename))
        return

    p = Parser(input_filename)
    with open(output_filename, 'w') as fout:
        while True:
            if not p.has_more_commands():
                break

            p.advance()
            command = decode_command(p)
            fout.write(command + '\n')


def decimal_to_binary_str(dec_value):
    return format(dec_value, '015b')


def decode_command(p):
    command_type = p.command_type()
    command_decoded = ''
    c = Code()

    if command_type == 'L_COMMAND':
        command_decoded = p.symbol()
    elif command_type == 'A_COMMAND':
        symbol = p.symbol()
        if symbol in predefined_symbols:
            predefined_symbol = predefined_symbols[symbol]
            command_decoded = '0' + decimal_to_binary_str(predefined_symbol)
        else:
            command_decoded = '0' + decimal_to_binary_str(int(symbol))

    elif command_type == 'C_COMMAND':
        command_decoded = '111' + \
            c.comp(p.comp()) + c.dest(p.dest()) + c.jump(p.jump())

    return command_decoded


def get_full_input_filename():
    try:
        input_filename = sys.argv[1]
        return os.path.abspath(os.path.join(input_filename))
    except IndexError:
        return None


def get_full_output_filename(input_filename):
    return input_filename[:-3] + 'hack'


if __name__ == "__main__":
    main()
