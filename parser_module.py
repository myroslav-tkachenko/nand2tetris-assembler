class Parser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.input_file = open(self.file_name)
        self.current_command = None
        self.next_command = self.input_file.readline()

    def __del__(self, *args):
        self.input_file.close()

    def advance(self):
        if self.has_more_commands():
            while True:
                self.current_command = self.next_command.split(
                    '//')[0].strip()
                self.next_command = self.input_file.readline()

                if self.current_command:
                    break

    def has_more_commands(self):
        return bool(self.next_command)

    def command_type(self):
        prefix = self.current_command[0]

        if prefix == '(':
            return 'L_COMMAND'
        elif prefix == '@':
            return 'A_COMMAND'
        else:
            return 'C_COMMAND'
