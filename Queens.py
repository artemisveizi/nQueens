import time
import math
import heapq
from collections import deque
import random
from random import shuffle
from copy import copy


class nQueens:
    def __init__(self, s, c, n):
        """ creates an nQueens board where state is a list of n integers,
            one per column,
            and choices is a list of sets,
            n is the size
            parent is the state predecessor in a search
        """
        if s is not None:                           # set all indices -1 for goal state checking later on
            self.state = s
        else:
            self.state = [-1] * n
        if c is not None:
            self.choices = c
        else:
            self.choices = [set(range(n))] * n
        self.size = n
        self.num_goal_tests = 0
        self.num_children = 0

    def assign(self, var, value):
        """ updates the state by setting state[var] to value
            also propgates constraints and updates choices
        """
        self.state[var] = value                     # puts a queen in this position
        self.choices[var] = set()                   # removes all choices from this column since it has a queen in it already
        for c in range(self.size):                  # removes this row option from all other columns so that no two queens are in the same column
            self.choices[c].discard(value)
        for c in range(self.size):                  # removes all diagonal options
            for r in range(self.size):
                if abs(var - c) == abs(value - r):
                    self.choices[c].discard(r)

    def goal_test(self):
        """ returns True iff state is the goal state """
        return -1 not in self.state

    def sort_by_dist(self, a):
        """ sorts the list a based on each element's distance
            to the center column of the board 
        """
        sorted = []
        while a:
            min_val = 1000
            min_var = 0
            for i in a:
                if math.fabs(i - (self.size / 2 - 1)) < min_val:
                    min_val = math.fabs(i - (self.size / 2 - 1))
                    min_var = i
            a.remove(min_var)
            sorted.append(min_var)
        return sorted

    def get_next_unassigned_var_dfs(self):
        """ returns next available column """
        for i in range(len(self.state)):
            if self.state[i] == -1:
                return i
        return -1

    def get_choices_for_var_dfs(self, var):
        """ return sorted set of rows available for this column """
        return self.choices[var]

    def get_next_unassigned_var_mid(self): #HEURISTIC 2: MOST CONSTRAINED COLUMN FIRST
        """ first heuristic: choose columns based on proximity to center """
        a = []
        for i in range(self.size):
            if self.state[i] == -1:
                a.append(i)
        if a is not None:
            return a[int( (len(a) - 1) /2)]
        return null

    def get_choices_for_var_mid(self, var):
        """ first heuristic: rows selected based on proximity to center """    
        a = []
        for x in sorted(self.choices[var]):
            a.append(x)
        return self.sort_by_dist(a)

    def get_next_unassigned_var_rand(self): # HEURISTIC 1: COLUMNS CHOSEN RANDOMLY
        """ second heuristic: choose columns randomly """
        a = []
        for i in range(self.size):
            if self.state[i] == -1:
                a.append(i)
        if a is not None:
            shuffle(a)
            return a[0]
        return null

    def get_choices_for_var_rand(self, var):
        """ second/third heuristic: choose rows randomly """    
        a = list(self.choices[var])
        shuffle(a)
        return a

    def get_next_unassigned_var_most_constrained(self):
        """ third/fourth heuristic: returns the index of a column that is 
                most constrained """
        a = []
        min_options = self.size + 1
        min_ind = -1
        for i in range(self.size):
            if self.state[i] == -1:
                if min_options > len(self.choices[i]):
                    min_options = len(self.choices[i])
                    min_ind = i
        return min_ind

    def get_choices_for_var_most_constrained(self, var):
        """ fourth heuristic: returns choices[var], the list of available values
                 for variable var, possibly sorted """
        a = [0] * self.size
        for r in range(len(a)):
            for c in range(len(self.choices)):
                if r in self.choices[c] and r in self.choices[var]:
                    a[r] = a[r] + 1
        tr = []
        for i in range(len(a)):
            if a[i] is not 0:
                tr.append(i)
        return tr

    def __str__(self):
        """ returns a useful board-like string representation of the object """
        strn = ""
        for n in range(self.size):
            strn += ""
            for f in range(self.size):
                if self.state[n] is not f:
                    strn += " -"
                else:
                    strn += " Q"
            strn += "\n"
        return strn


# each method for the heuristics. basic DFS algorithm does not change.
def dfs_search(board):
    fringe = deque([])
    current = board
    while True:
        if current.goal_test():
            print(board.num_goal_tests)
            return current
        else:
            col = current.get_next_unassigned_var_dfs()
            if col is not None:
                for row in current.get_choices_for_var_dfs(col):
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
        if not fringe:
            return False
        current = fringe.pop()

def mid_search(board):
    fringe = deque([])
    current = board
    while True:
        if current.goal_test():
            return current
        else:
            col = current.get_next_unassigned_var_mid()
            if col is not None:
                for row in current.get_choices_for_var_mid(col):
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
        if not fringe:
            return False
        current = fringe.pop()

def rand_search(board):
    fringe = deque([])
    current = board
    while True:
        if current.goal_test():
            print(board.num_goal_tests)
            return current
        else:
            col = current.get_next_unassigned_var_rand()
            if col is not None:
                for row in current.get_choices_for_var_rand(col):
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
        if not fringe:
            return False
        current = fringe.pop()

def mc_search(board):
    fringe = deque([])
    current = board
    while True:
        if current.goal_test():
            return current
        else:
            col = current.get_next_unassigned_var_most_constrained()
            if col is not None:
                for row in current.get_choices_for_var_rand(col):
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
        if not fringe:
            return False
        current = fringe.pop()

def e_search(board):
    fringe = deque([])
    current = board
    while True:
        if current.goal_test():
            return current
        else:
            col = current.get_next_unassigned_var_most_constrained()
            if col is not None and board.num_goal_tests > board.size: # to ensure that I am not simply returning the same board everytime
                for row in current.get_choices_for_var_most_constrained(col):
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
            elif col is not None:
                for row in current.get_choices_for_var_rand(col): # randomize the first few children to create variability for testing purposes
                    newchoices = [x.copy() for x in current.choices]
                    child = nQueens(current.state.copy(), newchoices, current.size)
                    child.assign(col, row)
                    board.num_children = board.num_children + 1
                    board.num_goal_tests = board.num_goal_tests + 1
                    if child.goal_test():
                        print(board.num_children)
                        print(board.num_goal_tests)
                        return child
                    else:
                        fringe.append(child)
        if not fringe:
            return False
        current = fringe.pop()
"""
print("DFS")
for i in range(6):
    start_time = time.time()
    board = dfs_search(nQueens(None, None, 3 * i + 1))
    print(board)
    end_time = time.time()
    print("Total time: " + str(end_time - start_time) + "\n" + "\n")

print("MID SEARCH")
for i in range (10):
    mid_start_time = time.time()
    board = mid_search(nQueens(None, None, 3 * i + 1))
    mid_end_time = time.time()
    print(board)
    print("Total time: " + str(mid_end_time - mid_start_time) + "\n" + "\n")

print("RAND SEARCH")
for i in range(10):
    rand_start_time = time.time()
    board = rand_search(nQueens(None, None, i * 3 + 1))
    rand_end_time = time.time()
    print(board)
    print("Total time: " + str(rand_end_time - rand_start_time) + "\n" + "\n")

print("MC_SEARCH")
for i in range (15):
    mc_start_time = time.time()
    board = mc_search(nQueens(None, None, 49))
    print(board)
    mc_end_time = time.time()
    print("Total time: " + str(mc_end_time - mc_start_time) + "\n" + "\n")
"""
print("E_SEARCH")
for i in range (20):
    mc_start_time = time.time()
    board = e_search(nQueens(None, None, 3 * i + 1))
    print(board)
    mc_end_time = time.time()
    print("Total time: " + str(mc_end_time - mc_start_time) + "\n" + "\n")
