class PrettyPrinter:
    """A class to pretty print text to the console using ANSI color codes."""
    def __init__(self):
        self.black = "\033[0;30m"
        self.red = "\033[0;31m"
        self.green = "\033[0;32m"
        self.brown = "\033[0;33m"
        self.blue = "\033[0;34m"
        self.purple = "\033[0;35m"
        self.cyan = "\033[0;36m"
        self.light_gray = "\033[0;37m"
        self.dark_gray = "\033[1;30m"
        self.light_red = "\033[1;31m"
        self.light_green = "\033[1;32m"
        self.yellow = "\033[1;33m"
        self.light_blue = "\033[1;34m"
        self.light_purple = "\033[1;35m"
        self.light_cyan = "\033[1;36m"
        self.light_white = "\033[1;37m"
        self.bold = "\033[1m"
        self.faint = "\033[2m"
        self.italic = "\033[3m"
        self.underline = "\033[4m"
        self.crossed = "\033[9m"
        self.end = "\033[0m"

    def bold(self, message):
        print(self.bold + message + self.end)

    def underline(self, message):
        print(self.underline + message + self.end)

    def black(self, message):
        print(self.black + message + self.end)
        
    def red(self, message):
        print(self.red + message + self.end)
        
    def green(self, message):
        print(self.green + message + self.end)
        
    def brown(self, message):
        print(self.brown + message + self.end)
    
    def blue(self, message):
        print(self.blue + message + self.end)
        
    def purple(self, message):
        print(self.purple + message + self.end)
        
    def cyan(self, message):
        print(self.cyan + message + self.end)
        
    def light_gray(self, message):
        print(self.light_gray + message + self.end)
        
    def dark_gray(self, message):
        print(self.dark_gray + message + self.end)
    
    def light_red(self, message):
        print(self.light_red + message + self.end)
    
    def light_green(self, message):
        print(self.light_green + message + self.end)
    
    def yellow(self, message):
        print(self.yellow + message + self.end)
        
    def light_blue(self, message):
        print(self.light_blue + message + self.end)
        
    def light_purple(self, message):
        print(self.light_purple + message + self.end)
        
    def light_cyan(self, message):
        print(self.light_cyan + message + self.end)
    
    def light_white(self, message):
        print(self.light_white + message + self.end)
    
    def bold(self, message):
        print(self.bold + message + self.end)
        
    def faint(self, message):
        print(self.faint + message + self.end)
        
    def italic(self, message):
        print(self.italic + message + self.end)
        
    def underline(self, message):
        print(self.underline + message + self.end)
        
    def crossed(self, message):
        print(self.crossed + message + self.end)
