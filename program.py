import sys
import os
from parser_module import Parser
from code_module import Code
from symbols_module import SymbolTable


def main():
    input_filename = get_full_input_filename()
    output_filename = get_full_output_filename(input_filename)

    if not input_filename:
        print('You need to specify an input filename.')
        return

    if not os.path.exists(input_filename):
        print('The file {} does not exists.'.format(input_filename))
        return

    # parse labels
    st = SymbolTable()

    p0 = Parser(input_filename)
    position_address = 0

    while True:
        if not p0.has_more_commands():
            break

        p0.advance()
        command_type = p0.command_type()
        symbol = p0.symbol()
        position_address += 1

        if command_type == 'L_COMMAND':
            position_address -= 1
            if not st.contains(symbol):
                st.add_entry(symbol, position_address)

    # parse addresses
    p1 = Parser(input_filename)
    variable_address = 16

    while True:
        if not p1.has_more_commands():
            break

        p1.advance()
        command_type = p1.command_type()
        symbol = p1.symbol()

        if command_type == 'A_COMMAND':
            if not st.contains(symbol) and not is_number(symbol):
                st.add_entry(symbol, variable_address)
                variable_address += 1

    # second pass
    p2 = Parser(input_filename)
    with open(output_filename, 'w') as fout:
        while True:
            if not p2.has_more_commands():
                break

            p2.advance()
            command = decode_command(p2, st)
            if command:
                fout.write(command + '\n')


def decimal_to_binary_str(dec_value):
    return format(dec_value, '015b')


def is_number(string):
    try:
        int(string)
        return True
    except:
        return False


def decode_command(p, st):
    command_type = p.command_type()
    command_decoded = None
    c = Code()

    if command_type == 'A_COMMAND':
        symbol = p.symbol()
        if st.contains(symbol):
            symbol_value = st.get_address(symbol)
            command_decoded = '0' + decimal_to_binary_str(symbol_value)
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
