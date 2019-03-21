import sys
import os
from parser_module import Parser


def get_full_input_filename():
    try:
        input_filename = sys.argv[1]
        return os.path.abspath(os.path.join(input_filename))
    except IndexError:
        return None


def main():
    input_filename = get_full_input_filename()

    if not input_filename:
        print('You need to specify an input filename.')
        return

    if not os.path.exists(input_filename):
        print('The file {} does not exists.'.format(input_filename))
        return

    p = Parser(input_filename)

    while True:
        if not p.has_more_commands():
            break
        p.advance()
        print("Command: \'{}\' of Type: {}".format(
            p.current_command, p.command_type()))


if __name__ == "__main__":
    main()
