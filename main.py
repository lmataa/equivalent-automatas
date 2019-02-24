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
    Transforms <A> into a Deterministic Finite Automata <Aux> 
    :param A: an automata (DFA or NDFA)
    :output A': a DFA
    '''
    Aux = {'q': 0, 'Q': 1, 'F': [], 'A': ['a', 'b'], 'f': { 0: {'a': [], 'b': [] } } } #The transformed automata at the start of the process

    statesAux = [set([0])] # This list will hold the posible combinations of states from A that form one Aux state, contains the state 0 at first
    statesAuxNotUsed = [set([0])] #This list will hold the combinations that we haven't searched through yet

    #Sets are used for combinations as they hold no order

    while(len(statesAuxNotUsed)!=0): #This process will repeat itself until all posible combinations of states from A that form Aux are examinated 
        
        combination = statesAuxNotUsed.pop(0) #combination now holds the combination that is being used
        Aux['f'].update({statesAux.index(combination): {'a': [], 'b': []}}) #The structure to hold the connections is prepared
        
        #print(f"This is the combination from A: {combination}")
        
        #Now we have to find what other states is that combination connected through a letter in A

        for letter in A['A']:

            newCombination=set() #This set holds all the states that can be accessed through letter from combination

            for state in combination: #we cycle through each state in combination and add the new states that can be accesed

                newCombination.update(A['f'][state][letter])
            """
            Now that we have the combination we have to include it in the list of statesAux and statesAuxNot used if it wasn't before
            and in Aux connect the combination through letter to new combination.
            the indexes for both will be their position in statesAux
            """
            #print(f"This is connected in Aux to {newCombination}")
            if newCombination != set():
                if newCombination not in statesAux:
                    statesAux.append(newCombination)
                    statesAuxNotUsed.append(newCombination)
                    #print("needs to be added")
                    #print(f"Added to statesAux {statesAux} and statesAuxNotUsed {statesAuxNotUsed}")

                #print(f"This combination is in the position {statesAux.index(combination)}")
                
                Aux['f'][statesAux.index(combination)][letter] = [statesAux.index(newCombination)]

                for element in newCombination:
                    if element in A['F'] and statesAux.index(newCombination) not in Aux['F']: #We add the index to the final states if some state in newcombination is final and the newCombination is not present
                        Aux['F'].append(statesAux.index(newCombination))


    
    #We add the total number of states to Q

    Aux['Q'] = len(statesAux)

    return Aux

def complete_DFA(A1, A2):
    '''
    Comment
    '''
    return complete_DFA_aux(A1), complete_DFA_aux(A2)

def complete_DFA_aux(A):
    '''
    Transforms <A> into a complete DFA. We already know here that A is not complete
    :param A: a DFA
    :output A': a complete DFA
    '''
    added_death_state = False
    for state in A['f']:
        for transition in A['f'][state]:
            if len(A['f'][state][transition]) == 0: # The pair (state, transition) is not defined
                if not added_death_state: # Quicker than checking if <A> is not complete prior to getting into the loop
                    death_state = A['Q'] # Death state or sink hole
                    A['Q'] += 1 
                    added_death_state = True
                A['f'][state][transition].append(death_state) # Transition to death state
    return A
                

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
    F_ = []
    for q in range(0, A['Q']):
        if q not in A['F']: # We just have to reverse final and non-final states
            F_.append(q)
    A['F'] = F_
    return A


def obtain_intersection(A1, A2):
    '''
    Obtains the automata, named I, resulting from the intersection of A1 and A2
    :param A1: a complete DFA
    :param A2: a complete DFA
    :output I: intersection of A1 and A2
    '''
    # TODO: ===============================================================\
            
    # A2['f'][5]={ 'a':[], 'b':[]} # Hay que arreglar la salida del método anterior a este (o el anterior)
    k = A2['Q']
    if(len(A2['f'])+1==k):
        A2['f'][k-1]={'a':[], 'b':[]}
    k = A1['Q']
    if(len(A1['f'])+1==k):
        A1['f'][k-1]={'a':[], 'b':[]} 
    # TODO: ===============================================================/
    # print(A1)
    # print(A2)

    return cross_product(A1, A2)

def cross_product(A, B):
    assert(A['A'] == B['A']) # they need to have the same alphabet
    
    Q_AnB = [] # States
    for s1 in range(A['Q']): 
        for s2 in range(B['Q']):
            Q_AnB.append((s1, s2)) # all states
    
    q_AnB = (A['q'], B['q']) # initial states
   

    F_AnB = [] # Accepted states 
    for(s1, s2) in Q_AnB:
        if s1 in A['F'] and s2 in B['F']:
            F_AnB.append((s1,s2))
    
    #Intersection automata
    R={'q': q_AnB,
       'Q': len(Q_AnB),
       'F': F_AnB,
       'A': A['A'],
       'f':{}}
    '''
    print('1: States: ') 
    print(Q_AnB)
    print('2: Initial states:')
    print(q_AnB)
    print('3: Accepted states:')
    print(F_AnB)
    print('3: Algorithm:')
    '''
    # algorithm for delta transitions
    for (s1,s2) in Q_AnB:
        a_s1 = A['f'][s1]['a']
        b_s1 = A['f'][s1]['b']
        a_s2 = B['f'][s2]['a']
        b_s2 = B['f'][s2]['b']
        '''  
        print((s1,s2))
        print('init:')
        print('a_s1:')
        print(a_s1)
        print('b_s1:')
        print(b_s1)
        print('a_s2')
        print(a_s2)
        print('b_s2')
        print(b_s2)
        '''   
        a_comb=[]
        b_comb=[]
        if a_s1 != [] and a_s2 != []:
            for i in a_s1:
                for j in a_s2:
                    a_comb.append((i,j))
        
        if b_s1 != [] and b_s2 != []:
            for i in b_s1:
                for j in b_s2:
                    b_comb.append((i,j))
        
        R['f'][(s1,s2)]={'a': a_comb, 'b': b_comb}
        ''' 
        print (R)
        print((s1,s2))
        print('end')
        ''' 
    return R 



def language_is_empty(A):
    '''
    Checks if the accepted language of a given automata is empty/none
    :param A: an automata
    :output boolean: True if its language is empty, False otherwise
    '''
    print('esto es una traza para antes de que pete: linea 230, hacer algo para que los diccionarios acepten \n algo (s1,s2) como key porque sino infierno, el automata se crea bien')
    S = set() # Will hold ccessible states of <A> at the end
    S.add(A['q'])
    t = set()       
    count = 0
    
    while len(S) < A['Q'] and count < A['Q']:
        count += 1
        for state in S:
            for transition in A['f'][state]:
                t.update(A['f'][state][transition]) # Accessible states from <S>
        S.update(t)
        t.clear()
    for state in A['F']:
        if state in S:
            return False
    return True

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
                default=0)
    parser.add_argument("-a2", "--automata-2", help="Automata 2, from the available list (0, 1, 2, 3)", type=int,
                default=1)

def main(A1, A2):
    '''
    This method will control the execution flow of the algorithm, consecutively calling the required methods to state if A1 and A2 are equal
    :param A1: an automata
    :param A2: an automata
    :output boolean: True if equal, False otherwise
    '''
    util.print_verbose(f"\nInitial automatas: \n\t{A1} \n\t{A2}")
    A1, A2 = transform_DFA(A1, A2)
    util.print_verbose(f"\n1. Transformation: \n\tA1: \n\t\t{A1} \n\tA2: \n\t\t{A2}")
    A1, A2 = complete_DFA(A1, A2)
    util.print_verbose(f"\n2. Completion: \n\tA1: \n\t\t{A1} \n\tA2: \n\t\t{A2}")
    B1, B2 = obtain_complement(A1, A2)
    util.print_verbose(f"\n3. Complements: \n\tB1 (complement of A1): \n\t\t{B1} \n\tB2 (complement of A2): \n\t\t{B2}")
    I = obtain_intersection(A1, B2)
    print("Autómata de la intersección: ")
    print(I)
    util.print_verbose(f"\n4. Intersections: \n\tA1 and B2: \n\t\t{I} ")
    return (language_is_empty(I))
    

class automatas:
    '''
    - q: initial state
    - Q: states
    - F: final states
    - A: alphabet
    - f: transitions
    '''
    
    A1 = {
        'q': 0,
        'Q': 4,
        'S': [0, 1, 2, 3],
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

    A4 ={
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
            equivalent = main(A1 = automatas.automata[args.automata_1], A2 = automatas.automata[args.automata_2])
            if equivalent:
                util.print_color("Equivalent!", bcolors.OKGREEN)
            else:
                util.print_color("Not equivalent!", bcolors.OKBLUE)
        else:
            util.print_color("[!] Not a valid automata", bcolors.FAIL)
    except Exception as e:
        util.print_color("[-] An error ocurred!", bcolors.FAIL)
        util.print(e)
    
