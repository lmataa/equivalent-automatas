import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class utilities():
    def __init__(self, arguments):
        self.quiet = arguments.quiet
        self.verbose = arguments.verbose
        self.no_color = arguments.no_color

    def print_verbose(self, string):
        if self.verbose:
            self.print(string)

    def print_color(self, string, bcolor=None):
        if not self.no_color:
            self.print(bcolor + string + bcolors.ENDC)

    def print_verbose_color(self, string, bcolor=None):
        if self.verbose and not self.no_color:
            self.print(bcolor + string + bcolors.ENDC)
        elif self.verbose:
            self.print(string)

    def print(self, string):
        if not self.quiet:
            print(string)

    def pprint(self, lines_data, output_file):
        if not output_file:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(lines_data)

def main(A1, A2):


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path-chromedriver", help="Path where chromedriver is stored", type=str,
                        default=PATH_CHROMEDRIVER)
    parser.add_argument("-o", "--output", help="If not specified, no output will be produced", action="store_true")
    parser.add_argument("-nc", "--no-color", help="Do not colorize output", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet, no output on terminal", action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="Be verbose. Useful when performing on slow network connections to know that it is working "
                            "and not dead",
                        action="store_true")
    