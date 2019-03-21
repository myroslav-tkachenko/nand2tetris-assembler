class Parser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.input_file = open(self.file_name)
        self.current_command = None
        self.next_command = self.input_file.readline()

    def __del__(self, *args):
        self.input_file.close()

    def advance(self):
        if not self.has_more_commands():
            return

        while True and self.has_more_commands():
            self.current_command = self.next_command.split(
                '//')[0].strip()
            self.next_command = self.input_file.readline()

            if self.current_command:
                break

    def has_more_commands(self):
        return bool(self.next_command)

    def command_type(self):
        try:
            prefix = self.current_command[0]
        except:
            return None

        if prefix == '(':
            return 'L_COMMAND'
        elif prefix == '@':
            return 'A_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        try:
            prefix = self.current_command[0]
        except:
            return None

        if prefix == '(':
            return self.current_command[1:-1]
        elif prefix == '@':
            return self.current_command[1:]

    def dest(self):
        has_dest = self.current_command.find('=') > -1

        if has_dest:
            return self.current_command.split('=')[0]
        else:
            return None

    def comp(self):
        has_dest = self.current_command.find('=') > -1
        has_jump = self.current_command.find(';') > -1

        if has_dest:
            command = self.current_command.split('=')[1]
        else:
            command = self.current_command

        if has_jump:
            return command.split(';')[0]
        else:
            return command

    def jump(self):
        has_jump = self.current_command.find(';') > -1

        if has_jump:
            return self.current_command.split(';')[1]
        else:
            return None
