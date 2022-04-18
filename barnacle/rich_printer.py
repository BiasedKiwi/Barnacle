class PrettyPrinter:
    """A class to pretty print text to the console using ANSI color codes."""

    def __init__(self):
        self._black = "\033[0;30m"
        self._red = "\033[0;31m"
        self._green = "\033[0;32m"
        self._brown = "\033[0;33m"
        self._blue = "\033[0;34m"
        self._purple = "\033[0;35m"
        self._cyan = "\033[0;36m"
        self._light_gray = "\033[0;37m"
        self._dark_gray = "\033[1;30m"
        self._light_red = "\033[1;31m"
        self._light_green = "\033[1;32m"
        self._yellow = "\033[1;33m"
        self._light_blue = "\033[1;34m"
        self._light_purple = "\033[1;35m"
        self._light_cyan = "\033[1;36m"
        self._light_white = "\033[1;37m"
        self._bold = "\033[1m"
        self._faint = "\033[2m"
        self._italic = "\033[3m"
        self._underline = "\033[4m"
        self._crossed = "\033[9m"
        self.end = "\033[0m"

    def bold(self, message):
        print(self._bold + message + self.end)

    def underline(self, message):
        print(self._underline + message + self.end)

    def black(self, message):
        print(self._black + message + self.end)

    def red(self, message):
        print(self._red + message + self.end)

    def green(self, message):
        print(self._green + message + self.end)

    def brown(self, message):
        print(self._brown + message + self.end)

    def blue(self, message):
        print(self._blue + message + self.end)

    def purple(self, message):
        print(self._purple + message + self.end)

    def cyan(self, message):
        print(self._cyan + message + self.end)

    def light_gray(self, message):
        print(self._light_gray + message + self.end)

    def dark_gray(self, message):
        print(self._dark_gray + message + self.end)

    def light_red(self, message):
        print(self._light_red + message + self.end)

    def light_green(self, message):
        print(self._light_green + message + self.end)

    def yellow(self, message):
        print(self._yellow + message + self.end)

    def light_blue(self, message):
        print(self._light_blue + message + self.end)

    def light_purple(self, message):
        print(self._light_purple + message + self.end)

    def light_cyan(self, message):
        print(self._light_cyan + message + self.end)

    def light_white(self, message):
        print(self._light_white + message + self.end)

    def bold(self, message):
        print(self._bold + message + self.end)

    def faint(self, message):
        print(self._faint + message + self.end)

    def italic(self, message):
        print(self._italic + message + self.end)

    def underline(self, message):
        print(self._underline + message + self.end)

    def crossed(self, message):
        print(self._crossed + message + self.end)
