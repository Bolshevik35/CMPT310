#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 25
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions

def literalList(clauses):
    literals = {}
    for clause in clauses:
        for lit in clause:
            if lit in literals:
                literals[lit] += 1
            else:
                literals[lit] = 1
	# for clause in clauses: 
	# 	for literal in clause:
 #            if literal in literals:
 #                literals[literal] += 1
 #            else:
 #                literals[literal] =1
    return literals

def varList(literals):
	varList = []
	for x in literals:
		if x < 0:
			temp = -1 * x 
			if temp not in varList: 
				varList.append(temp)
		else:
			if x not in varList:
				varList.append(x)
	return varList

def elimination_clauses(clauses, variable):
    newClauses = []
    if clauses == -1:
        return -1

    for each in clauses:
        if variable in each: 
            continue
        elif -variable in each:
            temp = [x for x in each if x != -variable]
            #temp = each
            #temp.remove(-variable)
            if len(temp) == 0:
                return -1
            newClauses.append(temp)
        else:
            newClauses.append(each)
    return newClauses

def pureLiterals(clauses):
    literals = literalList(clauses)
    for lit, times in literals.items():
        if -lit not in literals:
            return lit
    return -1

def unitPropagation(clauses):
    for clause in clauses:
        if len(clause) == 1:
            temp = clause[0]
            return temp
    return -1

def DPLL(clauses, variable, model):
    if not clauses:
        return True 
    if clauses == -1:
        return False

    varLi = copy.copy(variable)

    pureLit = pureLiterals(clauses)
    if pureLit != -1:
        if pureLit > 0:
            temp = varLi.remove(pureLit)
            #var = [x for x in variable if x != pureLit]
            model.update({pureLit : True})
            return DPLL(elimination_clauses(clauses, pureLit), varLi, model)
        else:
            temp = varLi.remove(-pureLit)
            #var = [x for x in variable if x != pureLit]
            model.update({pureLit : False})
            return DPLL(elimination_clauses(clauses, pureLit), varLi, model)

    unitClauses = unitPropagation(clauses)
    if unitClauses != -1:
        if unitClauses > 0:
            temp = varLi.remove(unitClauses)
            #var = [x for x in variable if x != unitClauses]
            model.update({unitClauses : True})
            return DPLL(elimination_clauses(clauses, unitClauses), varLi, model)
        else:
            temp = varLi.remove(-unitClauses)
            #var = [x for x in variable if x != unitClauses]
            model.update({unitClauses : False})
            return DPLL(elimination_clauses(clauses, unitClauses), varLi, model)

    p = varLi.pop()
    model.update({p:True})
    ret = DPLL(elimination_clauses(clauses, p), varLi, model)
    if not ret:
        model.update({p:False})
        ret = DPLL(elimination_clauses(clauses, -p), varLi, model)
    return ret

def solve_dpll(instance, verbosity):
    #print(instance)
    # instance.VARS goes 1 to N in a dict
    #print(instance.VARS)
    #print(verbosity)
    ###########################################
    # Start your code 
    clauses = instance.clauses
    #print(clauses)
    variables = instance.VARS
    ptr = {}
    ret = DPLL (clauses, variables, ptr)
    valueList = []
    for x, y in ptr.items():
        if y == True:
            valueList.append(x)
    valueList.sort()
    if ret == False:
    	print("UNSAT")
    elif verbosity == False: 
        print("SAT")
    else:
        print("SAT")
        print(valueList)





    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])
