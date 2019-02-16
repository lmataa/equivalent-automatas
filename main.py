import argparse
# TODO pprint is useful to print json and dictionary-based structures, but will not make its way to the final release.
# Remove this prior to final release
import pprint

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

    # TODO pprint is useful to print json and dictionary-based structures, but will not make its way to the final release.
    # Remove this prior to final release
    def pprint(self, lines_data, output_file):
        if not output_file:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(lines_data)

def transform_DFA(A):
    '''
    Checks if <A> is a DFA and transforms it into a Deterministic Finite Automata if its not
    :param A: an automata
    :output A': a DFA
    '''
    pass

def complete_DFA(A):
    '''
    Transforms <A> into a complete DFA
    :param A: a DFA
    :output A': a complete DFA
    '''
    pass

def obtain_complement(A):
    '''
    Obtains A's complement
    :param A: a complete DFA
    :output B: A's complement
    '''
    pass

def obtain_intersection(A1, A2):
    '''
    Obtains the automata, named I, resulting from the intersection of A1 and A2
    :param A1: a complete DFA
    :param A2: a complete DFA
    :output I: intersection of A1 and A2
    '''
    pass

def is_empty(A):
    '''
    Checks if the accepted language of a given automata is empty/none
    :param A: an automata
    :output boolean: True if its language is empty, False otherwise
    '''
    pass

def main(A1, A2):
    '''
    This method will control the execution flow of the algorithm, consecutively calling the required methods to state if A1 and A2 are equal
    :param A1: an automata
    :param A2: an automata
    :output boolean: True if equal, False otherwise
    '''
    pass

if __name__ == "__main__":
    # TODO: make this try-except block decent
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-nc", "--no-color", help="Do not colorize output", action="store_true")
        parser.add_argument("-q", "--quiet", help="Only True or False is printed", action="store_true")
        parser.add_argument("-v", "--verbose",
                            help="Print information as the algorithm progresses",
                            action="store_true")
        args = parser.parse_args()
        global util
        util = utilities(args)
    except Exception as e:
        util.print_color("[-] An error ocurred!", bcolors.FAIL)
        util.print_verbose(e)
    