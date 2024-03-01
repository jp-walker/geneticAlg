
# Jp Walker
# Using genetic algorithms to create better functioning picobot instructions, aiming to cover the entire map with picobot's movement
# 4/29/2022

import random
import copy

# class Program to represent a single Picobot program.
# class World to represent a single Picobot world
# self.rules[(0, "xExx")] = ("N", 1)

class Program:


    def __init__(self):
        """initializes that Program is an empty dictionary"""
        self.rules = {}

    def __repr__(self):
        """defines how to represent the class Program: the key will be printed, then an arrow, 
        then the value, then a new line, and so on."""
        rules = ""
        for k in self.rules:
            rules += str(k[0]) + " " + k[1] + " -> " + self.rules[k][0] + " " + str(self.rules[k][1]) + " \n"
        return rules

    def randomize(self):
        """generates a random, full set of rules for the program's self.rules dictionary.
        there will be 45 randomly generated rules for 9 possible surroundings and 5 different states.
        the keys are not random, only the values"""
        POSSIBLE_SURROUNDINGS = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        POSSIBLE_STEPS = {}
        KEYS = []
        NEW_RULES = {}
        for n in range(5):
            for e in range(len(POSSIBLE_SURROUNDINGS)):
                KEYS += [(n, POSSIBLE_SURROUNDINGS[e])]
        for i in range(len(KEYS)):
            for d in "NEWS":
                if d not in KEYS[i][1]:
                    if KEYS[i] not in POSSIBLE_STEPS:
                        POSSIBLE_STEPS[KEYS[i]] = [d]
                    else:
                        POSSIBLE_STEPS[KEYS[i]] += [d]
        for i in range(len(POSSIBLE_STEPS)):
            NEW_RULES[KEYS[i]] = (random.choice(POSSIBLE_STEPS[KEYS[i]]), random.choice(range(5)))
        
        self.rules = NEW_RULES

    def getMove(self, state, surroundings):
        """accepts an integer state and a surroundings (e.g., "xExx") and returns a tuple
        that contains the next move and the new state using the dictionary resulting from self.randomize()"""
        return self.rules[(state,surroundings)][0] + " " + str(self.rules[(state,surroundings)][1])

    def mutate(self):
        """chooses a random single rule from self.rules and changes the value for that rule to a different 
        but still legal value, and not the same value"""
        possible_keys = list(self.rules.keys())
        mutant = random.choice(range(len(possible_keys)))
        current_values = list(self.rules.values())
        POSSIBLE_STEPS = []
        ogkeys = copy.deepcopy(possible_keys)
        ogvalues = copy.deepcopy(current_values)


        for d in "NEWS":
            if d not in possible_keys[mutant][1]:
                POSSIBLE_STEPS += [str(d)]

        while current_values[mutant] == ogvalues[mutant]:
            current_values[mutant] = (random.choice(POSSIBLE_STEPS), random.choice(range(5)))
            self.rules[possible_keys[mutant]] = current_values[mutant]


    def crossover(self,other):
        """accepts an other object of type Program, and returns a new "offspring" Program that contains some of the rules 
        from self and the rest from other."""

        POSSIBLE_SURROUNDINGS = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        child = Program()
        parent1 = random.choice(range(0,4))
        for n in range(parent1+1):
            for i in range(len(POSSIBLE_SURROUNDINGS)):
                child.rules[n,POSSIBLE_SURROUNDINGS[i]] = self.rules[n,POSSIBLE_SURROUNDINGS[i]]
        for n in range(parent1+1,5):
            for i in range(len(POSSIBLE_SURROUNDINGS)):
                child.rules[n,POSSIBLE_SURROUNDINGS[i]] = other.rules[n,POSSIBLE_SURROUNDINGS[i]]
        return child


def population(n):
    """returns a list of random picobot Programs of length n"""
    L = []
    for n in range(n):
        p = Program()
        p.randomize()
        L += [p]
        
    return L

def evaluateFitness(program, trials, steps):
    """takes a program, number of times to test the program 
    (with random starting places each time), 
    and number of steps to execute each test.
    returns a float between 0.0 and 1.0 indicating the average of 
    how many cells of the board the picobot was able to cover"""
    fitness = 0.0
    for t in range(trials):
        w = World(random.choice(range(1,24)), random.choice(range(1,24)), program)
        w.run(steps)
        fitness += w.fractionVisitedCells()
    return (fitness/trials)

def GA(popsize, numgens):
    """creates a population size (of size popsize). then, it:
    evaluates the fitness of each program
    sorts a list of [fitness, program] tuples
    extracts the most-fit programs
    and creates (at random) crossovers of different programs from the most fit pool
    it will repeat this process as many times as numgens states, 
    and return the best program to have been made in the last generation
    """
    ogGen = population(popsize)
    newGen = []

    if numgens == 0:
        L = [(evaluateFitness(ogGen[i], 50, 1500),i) for i in range(len(ogGen))]
        best_index = max(L)[1]
        best_program = ogGen[best_index]
        fitness = [SL[n][0] for n in range(len(SL))]
        avfitness = sum(fitness)/len(fitness)
        print("Generation 0: ")
        print("     Average fitness: ", avfitness)
        print("     Best fitness:    ", max(fitness))                                              
        saveToFile(("gen" + str(0) + '.txt'), best_program)
    else:
        for gen in range(numgens+1):
            if gen == 0:
                L = [(evaluateFitness(ogGen[i], 50, 1500),i) for i in range(len(ogGen))]
                best_index = max(L)[1]
                best_program = ogGen[best_index]
                fitness = [L[n][0] for n in range(len(L))]
                avfitness = (sum(fitness)/len(fitness))
                print("Generation 0: ")
                print("     Average fitness: ", avfitness)
                print("     Best fitness:    ", max(fitness))                                              
                saveToFile(("gen" + str(0) + '.txt'), best_program)
                NL = copy.deepcopy(L)
            else:
                L = copy.deepcopy(NL)
                SL = sorted(L)                                                          
                cutoff = int(len(ogGen) - (.1*len(ogGen))) - 1          #added -1
                bestParents = SL[cutoff:]
                for n in range(len(bestParents)):
                    newGen += [ogGen[bestParents[n][1]]]
                for n in range(popsize - len(newGen)):
                    p1 = random.choice(range(len(bestParents)))
                    p2 = random.choice(list(range(0,p1)) + list(range(p1+1,len(bestParents))))
                    child = ogGen[bestParents[p1][1]].crossover(ogGen[bestParents[p2][1]])
                    mutation = random.choice(range(0,5))
                    for m in range(mutation):
                        child.mutate()
                    newGen += [child]
                NL = [(evaluateFitness(newGen[i], 50, 1500),i) for i in range(len(newGen))]
                best_index = max(NL)[1] 
                print("max L", max(L))
                print("max NL", max(NL))
                best_program = newGen[best_index]
                fitness = [NL[n][0] for n in range(len(NL))]
                avfitness = (sum(fitness)/len(fitness))
                ogGen = copy.deepcopy(newGen)
                newGen = []                                     
                print("Generation " + str(gen) + ": ")
                print("     Average fitness: ", avfitness)
                print("     Best fitness:    ", max(fitness))    
                saveToFile(("gen" + str(gen) + '.txt'), best_program)     


def saveToFile(filename, p):
        """Saves the data from Program p
           to a file named filename."""
        f = open(filename, "w")
        print(p, file = f)        # prints Picobot program from __repr__
        f.close()





HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

class World:

    def __init__(self, initial_row, initial_col, program):
        """initializes the class World"""

        self.row = initial_row
        self.col = initial_col
        self.state = 0
        self.program = program
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]
    
    def __repr__(self):
        """class World represents as a string that shows a room, with the character X as the walls, 
        the Picobot's location as a capital P, and lowercase o's to show empty but previously visited spaces.
        """

        """I was unsure because it said to start picobot at a random location, but the class World has 
        the initial row and column as part of it's argument... 
        so this is my code to generate random starting places from within the World class
        startCol = random.choice(range(1,WIDTH-2))
        startRow = random.choice(range(1,HEIGHT-2))

        self.row = startRow
        self.col = startCol"""

        for row in range(HEIGHT):
            for col in range(WIDTH):
                if col == 0 or col == (WIDTH-1):
                    self.room[row][col] = "X"
                elif row == 0 or row == (HEIGHT-1):
                    self.room[row][col] = "X"
                elif col == self.col and row == self.row:
                    self.room[row][col] = "P"
        
        string = ''

        for row in range(HEIGHT):                # row is the whole row
            for col in range(WIDTH): 
                if col == WIDTH-1:
                    string += str(self.room[row][col]) + "\n"
                else:
                    string += str(self.room[row][col])
            
        return string
    
    def getCurrentSurroundings(self):
        """returns a string in NEWS form of the current surroundings of picobot"""
        
        if self.col == 1 and self.row == 1:
            return "NxWx"
        elif self.col == 1 and self.row == HEIGHT-2:
            return "xxWS"
        elif self.col == WIDTH-2 and self.row == 1:
            return "NExx"
        elif self.col == WIDTH-2 and self.row == HEIGHT-2:
            return "xExS"
        elif self.col == WIDTH-2:
            return "xExx"
        elif self.col == 1:
            return "xxWx"
        elif self.row == 1:
            return "Nxxx"
        elif self.row == HEIGHT-2:
            return "xxxS"
        else:
            return "xxxx"

    def step(self):
        """moves the Picobot one step, updates self.room, and updates the state, row, and column of Picobot"""
        p = self.program
        position = self.getCurrentSurroundings()
        next = p.getMove(self.state, position)
        self.room[self.row][self.col] = "o"
        if next[0] == "N":
            self.row -= 1
        elif next[0] == "E":
            self.col += 1
        elif next[0] == "W":
            self.col -= 1
        elif next[0] == "S":
            self.row += 1
        
        self.state = int(next[2])

    def run(self, steps):
        """uses self.step() to execute the argument "steps" number of steps"""
        for s in range(steps):
            self.step()

    def fractionVisitedCells(self):
        """returns the fraction of cells of the room have been visited by picobot, including picobot's current location"""
        empty = 0
        visited = 0

        for row in range(1,HEIGHT-1):
            for col in range(1,WIDTH-1):
                if self.room[row][col] == " ":
                    empty += 1
                else:
                    visited += 1
        return float(visited/(visited + empty))