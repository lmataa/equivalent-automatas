import argparse
# TODO: pprint is useful to print json and dictionary-based structures, but will not make its way to the final release.
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

def transform_DFA(A1, A2):
    '''
    Comment
    '''
    return transform_DFA_aux(A1), transform_DFA_aux(A2)

def transform_DFA_aux(A):
    '''
    Checks if <A> is a DFA and transforms it into a Deterministic Finite Automata if its not
    :param A: an automata
    :output A': a DFA
    '''


    Aux = {'q': 0, 'Q': 1, 'F': [], 'A': ['a', 'b'], 'f': { 0: {'a': [], 'b': [] } } } #The transformed automata at the start of the process
    
    statesAux = [[0]] # This list will hold the posible combinations of states from A that form one Aux state, contains the state 0 at first
    statesAuxNotUsed = [[0]] #This list will hold the combinations that we haven't searched through yet

    while(len(statesAuxNotUsed)!=0):

        combination = statesAuxNotUsed.pop(0)
        Aux['f'].update({statesAux.index(combination): {'a': [], 'b': []}})


        for letter in A['A']:

            stateAux=set() #This set will hold the combination that later will be appended to statesAux, this is connected from combination by letter

            for state in combination:
                if len(A['f'][state][letter]) != 0:
                    for a in A['f'][state][letter]:
                        stateAux.add(a)

            stateAux = list(stateAux) #this now holds the states that can be accessed from combination thorugh letter
            if len(stateAux) > 0:
                statesAux, statesAuxNotUsed = isIn(statesAux, statesAuxNotUsed, stateAux)
                
                Aux['f'][statesAux.index(combination)][letter] = stateAux 
                #print(stateAux)
                
    print(Aux)
    pass

def isIn(statesAux, statesAuxNotUsed, combination): #This functions checks if a combination of states is in statesAux and returns its index, or if it is not it adds it to both StatesAux and StatesAuxNotUsed and returns its index on StatesAux
    
    """ Incomplete, the appending in case the combination is not present doesn't work"""
    position = 0
    inside = False
    
    for states in statesAux:
        
        insideAux = True
        if len(states) == len(combination):
            for state in combination:
                if not state in states:
                    insideAux = False
        else:
            insideAux = False
        
        if insideAux:
            inside = True
            position = statesAux.index(states)
        
    
    if not inside:
        statesAux.append(combination)
        statesAuxNotUsed.append(combination)        
    
    return statesAux, statesAuxNotUsed

def complete_DFA(A1, A2):
    '''
    Comment
    '''
    return complete_DFA_aux(A1), complete_DFA_aux(A2)

def complete_DFA_aux(A):
    '''
    Transforms <A> into a complete DFA
    :param A: a DFA
    :output A': a complete DFA
    '''

    pass

def obtain_complement(A1, A2):
    '''
    Comment
    '''
    return obtain_complement_aux(A1), obtain_complement_aux(A2)

def obtain_complement_aux(A):
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

def language_is_empty(A):
    '''
    Checks if the accepted language of a given automata is empty/none
    :param A: an automata
    :output boolean: True if its language is empty, False otherwise
    '''
    pass

def check_selection(A1, A2):
    try:
        if not max(A1, A2) < automatas.automata.__len__():
            raise Exception('Automata selection must be an integer smaller than {}. Instead, you selected {}'.format(str(automatas.automata.__len__()), str(max(A1, A2))))
        else:
            return True
    except TypeError as type_error:
        raise Exception('Automata selection must be an integer. Instead, you selected "{}" and "{}"'.format(str(A1), str(A2)))

def add_arguments(parser):
    parser.add_argument("-nc", "--no-color", help="Do not colorize output", action="store_true")
    parser.add_argument("-q", "--quiet", help="Only True or False is printed", action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="Print information as the algorithm progresses",
                        action="store_true")
    parser.add_argument("-a1", "--automata-1", help="Automata 1, from the available list (0, 1, 2, 3)", type=int,
                default=1)
    parser.add_argument("-a2", "--automata-2", help="Automata 2, from the available list (0, 1, 2, 3)", type=int,
                default=2)

def main(A1, A2):
    '''
    This method will control the execution flow of the algorithm, consecutively calling the required methods to state if A1 and A2 are equal
    :param A1: an automata
    :param A2: an automata
    :output boolean: True if equal, False otherwise
    '''
    A1, A2 = transform_DFA(A1, A2)
    A1, A2 = complete_DFA(A1, A2)
    B1, B2 = obtain_complement(A1, A2)
    I1, I2 = obtain_intersection(A1, B2), obtain_intersection(A2, B1)
    return (language_is_empty(I1) and language_is_empty(I2))
    

class automatas:
    '''
    - q0: initial state
    - Q: states
    - F: final states
    - A: alphabet
    - f: transitions
    '''
    A1 = {
        'q': 0,
        'Q': 4,
        'F': [3],
        'A': ['a', 'b'],
        'f': {
            0: {
                'a': [1],
                'b': [2]
            },
            1: {
                'a': [1],
                'b': [2]
            },
            2: {
                'a': [3],
                'b': [2]
            },
            3: {
                'a': [1],
                'b': [2]
            }
        }
    }

    A2 = {
        'q': 0,
        'Q': 5,
        'F': [1, 2, 3, 4],
        'A': ['a', 'b'],
        'f': {
            0: {
                'a': [1],
                'b': [2]
            },
            1: {
                'a': [],
                'b': [3],
            },
            2: {
                'a': [4],
                'b': []
            },
            3: {
                'a': [],
                'b': [3]
            },
            4: {
                'a': [4],
                'b': []
            }
        }
    }

    A3 = {
        'q': 0,
        'Q': 3,
        'F': [1, 2],
        'A': ['a', 'b'],
        'f': {
            0: {
                'a': [1],
                'b': [2]
            },
            1: {
                'a': [],
                'b': [1]
            },
            2: {
                'a': [2],
                'b': []
            }
        }
    }

    A4 = {
        'q': 0,
        'Q': 5,
        'F': [1, 2, 3, 4],
        'A': ['a', 'b'],
        'f': {
            0: {
                'a': [1],
                'b': [2]
            },
            1: {
                'a': [],
                'b': [3],
            },
            2: {
                'a': [4],
                'b': []
            },
            3: {
                'a': [],
                'b': [3]
            },
            4: {
                'a': [4],
                'b': []
            }
        }
    }
    automata = [A1, A2, A3, A4]


if __name__ == "__main__":
    # TODO: make this try-except block decent (nice exceptions control)
    try:
        parser = argparse.ArgumentParser()
        add_arguments(parser)
        args = parser.parse_args()
        global util
        util = utilities(args)
        if check_selection(args.automata_1, args.automata_2):
            main(A1 = automatas.automata[args.automata_1], A2 = automatas.automata[args.automata_2])
        else:
            util.print_color("[!] Not a valid automata", bcolors.FAIL)
    except Exception as e:
        util.print_color("[-] An error ocurred!", bcolors.FAIL)
        util.print(e)
    