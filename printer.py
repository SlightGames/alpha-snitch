class Printer(object):
    """ Utility class to help with indented printing """
    def __init__(self, silent=False):
        self.indent_size = 0
        self.indent_str = ""
        self.silent = silent

    def indent(self):
        self.indent_size += 1
        self.indent_str = "  " * self.indent_size

    def deindent(self):
        self.indent_size = max(0, self.indent_size - 1)
        self.indent_str = "  " * self.indent_size

    def print(self, what: str):
        if self.silent:
            return

        print(f"{self.indent_str}{what}")