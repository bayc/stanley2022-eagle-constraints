"""
some simple gradient-free optimization algorithms
"""
import numpy as np
import time
from math import log
from heapq import nsmallest
from itertools import filterfalse

def second_smallest(numbers):
    s = set()
    sa = s.add
    un = (sa(n) or n for n in filterfalse(s.__contains__, numbers))
    return nsmallest(2, un)[-1]


class GreedyAlgorithm():
    """a simple greedy algorithm
    """

    def __init__(self, bits, bounds, variable_type, objective_function,
                 consecutive_increases=2, start_index=None, start_ones=False,
                 args=None):
        """
        Parameters
        ----------
        bits : array of ints
            The number of bits assigned to each of the design variables.
            The number of discretizations for each design variables will be
            2^n where n is the number of bits assigned to that variable.
        bounds : array of tuples
            The bounds for each design variable. This parameter looks like:
            np.array([(lower, upper), (lower, upper)...])
        variable_type : array of strings ('int' or 'float')
            The type of each design variable (int or float).
        objective_function : function handle for the objective that is to be
            minimized. Should take a single variable as an input which is a
            list/array of the design variables.
        consecutive_increases : int, optional
            The number of consecutive objective increases to determine
            convergence.
        start_index : int, optional
            The index that will start as 1
        start_ones : bool, optional
            If true, the initial array will be all ones instead of all zeros
        """

        # inputs
        self.bits = bits
        self.bounds = bounds
        self.variable_type = variable_type
        self.objective_function = objective_function
        self.consecutive_increases = consecutive_increases
        self.start_index = start_index
        self.start_ones = start_ones
        self.args = args

        # internal variables, you could output some of this info if you wanted
        self.design_variables = np.array([])  # the desgin variables as they
        # are passed into self.objective function
        self.nbits = 0  # the total number of bits in each chromosome
        self.nvars = 0  # the total number of design variables
        self.discretized_variables = {}  # a dict of arrays containing all of
        # the discretized design variable

        # outputs
        self.solution_history = np.array([])
        self.optimized_function_value = 0.0
        self.optimized_design_variables = np.array([])

        self.initialize_design_variables()
        self.initialize_bits()


    def initialize_design_variables(self):
        """initialize the design variables from the randomly initialized
        population
        """
        # determine the number of design variables and initialize
        self.nvars = len(self.variable_type)
        self.design_variables = np.zeros(self.nvars)
        float_ind = 0
        for i in range(self.nvars):
            if self.variable_type[i] == "float":
                ndiscretizations = 2**self.bits[i]
                self.discretized_variables["float_var%s" % float_ind] = \
                    np.linspace(self.bounds[i][0], self.bounds[i][1],
                                ndiscretizations)
                float_ind += 1

    def initialize_bits(self):
        """determine the total number of bits"""
        # determine the total number of bits
        for i in range(self.nvars):
            if self.variable_type[i] == "int":
                int_range = (self.bounds[i][1] - self.bounds[i][0]) + 1
                int_bits = int(np.ceil(log(int_range, 2)))
                self.bits[i] = int_bits
            self.nbits += self.bits[i]

    def chromosome_2_variables(self, chromosome):
        """convert the binary chromosomes to design variable values"""

        first_bit = 0
        float_ind = 0

        for i in range(self.nvars):
            binary_value = 0
            for j in range(self.bits[i]):
                binary_value += chromosome[first_bit + j] * 2**j
            first_bit += self.bits[i]

            if self.variable_type[i] == "float":
                self.design_variables[i] = \
                    self.discretized_variables["float_var%s"
                                               % float_ind][binary_value]
                float_ind += 1

            elif self.variable_type[i] == "int":
                self.design_variables[i] = self.bounds[i][0] + binary_value
                if self.design_variables[i] > self.bounds[i][1]:
                    self.design_variables[i] = self.bounds[i][1]

    def optimize_greedy(self, print_progress=False):
        """run the greedy algorithm"""

        # initialize everything
        converged = False
        if self.start_ones:
            overall_best_binary = np.ones(self.nbits, dtype=int)
        else:
            overall_best_binary = np.zeros(self.nbits, dtype=int)
            if self.start_index is not None:
                overall_best_binary[self.start_index] = 1

        self.chromosome_2_variables(overall_best_binary)
        if self.args:
            overall_best_fitness = \
                self.objective_function(self.design_variables, self.args)
        else:
            overall_best_fitness = \
                self.objective_function(self.design_variables)
        self.solution_history = np.array([overall_best_fitness])
        n_increase = 0

        # base_iteration_binary
        # base_iteration_fitness

        # best_new_binary
        # best_new_fitness

        # overall_best_binary
        # overall_best_fitness

        base_iteration_binary = np.zeros_like(overall_best_binary)
        base_iteration_binary[:] = overall_best_binary[:]
        base_iteration_fitness = overall_best_fitness

        iteration = 0
        while converged is False:

            order = np.arange(self.nbits)
            np.random.shuffle(order)
            best_new_fitness = abs(base_iteration_fitness) * 1E6
            for i in range(self.nbits):
                temp_binary = np.zeros_like(base_iteration_binary)
                temp_binary[:] = base_iteration_binary[:]
                temp_binary[order[i]] = (temp_binary[order[i]] + 1) % 2
                self.chromosome_2_variables(temp_binary)
                if self.args:
                    temp_fitness = \
                        self.objective_function(self.design_variables, self.args)
                else:
                    temp_fitness = \
                        self.objective_function(self.design_variables)
                
                if temp_fitness < best_new_fitness:
                    best_new_fitness = temp_fitness
                    best_new_binary = np.zeros_like(temp_binary)
                    best_new_binary[:] = temp_binary[:]
            

            self.solution_history = np.append(self.solution_history, best_new_fitness)
            if best_new_fitness < overall_best_fitness:
                print("IMPROVED")
                overall_best_fitness = best_new_fitness
                overall_best_binary = np.zeros_like(best_new_binary)
                overall_best_binary[:] = best_new_binary[:]
                n_increase = 0
            else:
                print("NO IMPROVEMENT")
                n_increase += 1
            
            if n_increase >= self.consecutive_increases:
                converged = True
            else:
                base_iteration_fitness = best_new_fitness
                base_iteration_binary = np.zeros_like(best_new_binary)
                base_iteration_binary[:] = best_new_binary[:]
            
            iteration += 1
            if print_progress:
                print("best binary: ", repr(overall_best_binary))
                print("iteration: ", iteration)
                print("best solution: ", overall_best_fitness)
                print("_______________________")
                

        self.optimized_function_value = overall_best_fitness
        self.chromosome_2_variables(overall_best_binary)
        self.optimized_design_variables = self.design_variables

