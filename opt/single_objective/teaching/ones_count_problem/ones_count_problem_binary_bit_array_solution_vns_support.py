""" 
..  _py_ones_count_problem_bit_array_solution_vns_support:

The :mod:`~opt.single_objective.teaching.ones_count_problem.ones_count_problem_binary_bit_array_solution_vns_support` 
contains class :class:`~opt.single_objective.teaching.ones_count_problem.ones_count_problem_binary_bit_array_solution_vns_support.OnesCountProblemBinaryBitArraySolutionVnsSupport`, 
that represents supporting parts of the `VNS` algorithm, where solution of the :ref:`Problem_Max_Ones` have `BitArray` 
representation.
"""

import sys
from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent.parent)

from copy import deepcopy
from random import choice
from random import random

from bitstring import Bits, BitArray, BitStream, pack

from uo.utils.logger import logger
from uo.utils.complex_counter_uniform_distinct import ComplexCounterUniformAscending

from uo.target_solution.quality_of_solution import QualityOfSolution
from uo.algorithm.algorithm import Algorithm
from uo.algorithm.metaheuristic.variable_neighborhood_search.problem_solution_vns_support import ProblemSolutionVnsSupport

from opt.single_objective.teaching.ones_count_problem.ones_count_problem import OnesCountProblem
from opt.single_objective.teaching.ones_count_problem.ones_count_problem_binary_bit_array_solution import OnesCountProblemBinaryBitArraySolution

class OnesCountProblemBinaryBitArraySolutionVnsSupport(ProblemSolutionVnsSupport[BitArray,str]):
    
    def __init__(self)->None:
        """
        Create new `OnesCountProblemBinaryBitArraySolutionVnsSupport` instance
        """

    def __copy__(self):
        """
        Internal copy of the `OnesCountProblemBinaryBitArraySolutionVnsSupport`

        :return: new `OnesCountProblemBinaryBitArraySolutionVnsSupport` instance with the same properties
        :rtype: `OnesCountProblemBinaryBitArraySolutionVnsSupport`
        """
        sol = deepcopy(self)
        return sol

    def copy(self):
        """
        Copy the `OnesCountProblemBinaryBitArraySolutionVnsSupport` instance

        :return: new `OnesCountProblemBinaryBitArraySolutionVnsSupport` instance with the same properties
        :rtype: `OnesCountProblemBinaryBitArraySolutionVnsSupport`
        """
        return self.__copy__()

    def shaking(self, k:int, problem:OnesCountProblem, solution:OnesCountProblemBinaryBitArraySolution, 
            optimizer:Algorithm)->bool:
        """
        Random shaking of k parts such that new solution code does not differ more than k from all solution codes 
        inside shakingPoints 

        :param int k: int parameter for VNS
        :param `OnesCountProblem` problem: problem that is solved
        :param `OnesCountProblemBinaryBitArraySolution` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        :return: if randomization is successful
        :rtype: bool
        """    
        if optimizer.finish_control.check_evaluations \
                and optimizer.evaluation > optimizer.finish_control.evaluations_max:
            return False
        tries:int = 0
        limit:int = 10000
        while tries < limit:
            repres:BitArray = BitArray(solution.representation)
            positions:list[int] = []
            for _ in range(0,k):
                positions.append(choice(range(len(repres))))
            for pos in positions:
                repres.invert(pos)
            solution.representation = repres
            all_ok:bool = True
            if solution.representation.count(value=1) > problem.dimension:
                all_ok = False
            if all_ok:
                break
        if tries < limit:
            optimizer.evaluation += 1
            if optimizer.finish_control.check_evaluations and optimizer.evaluation > optimizer.finish_control.evaluations_max:
                return False
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            solution.evaluate(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            optimizer.write_output_values_if_needed("after_step_in_iteration", "shaking")
            return True
        else:
            return False 

    def local_search_best_improvement(self, k:int, problem:OnesCountProblem, solution:OnesCountProblemBinaryBitArraySolution, 
            optimizer: Algorithm)->OnesCountProblemBinaryBitArraySolution:
        """
        Executes "best improvement" variant of the local search procedure 
        
        :param int k: int parameter for VNS
        :param `OnesCountProblem` problem: problem that is solved
        :param `OnesCountProblemBinaryBitArraySolution` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        :return: result of the local search procedure 
        :rtype: OnesCountProblemBinaryBitArraySolution
        """
        if optimizer.finish_control.check_evaluations and optimizer.evaluation > optimizer.finish_control.evaluations_max:
            return solution
        if k < 1 or k > problem.dimension:
            return solution
        best_rep:BitArray = None
        best_qos:QualityOfSolution =  QualityOfSolution(solution.objective_value, None,
                solution.fitness_value, None, solution.is_feasible)
        # initialize indexes
        indexes:ComplexCounterUniformAscending = ComplexCounterUniformAscending(k, problem.dimension)
        in_loop:bool = indexes.reset()
        while in_loop:
            # collect positions for inversion from indexes
            positions:list[int] = indexes.current_state()
            # invert and compare, switch of new is better
            solution.representation.invert(positions) 
            optimizer.evaluation += 1
            if optimizer.finish_control.check_evaluations and optimizer.evaluation > optimizer.finish_control.evaluations_max:
                return solution
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            new_qos:QualityOfSolution = solution.calculate_quality(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            if QualityOfSolution.is_first_fitness_better(new_qos, best_qos, problem.is_minimization):
                best_qos = new_qos
                best_rep = BitArray(bin=solution.representation.bin)
            solution.representation.invert(positions)
            # increment indexes and set in_loop according to the state
            in_loop = indexes.progress()
        if best_rep is not None:
            solution.representation = best_rep
            solution.objective_value = best_qos.objective_value
            solution.fitness_value = best_qos.fitness_value
            solution.is_feasible = best_qos.is_feasible
            return solution
        return solution

    def local_search_first_improvement(self, k:int, problem:OnesCountProblem, solution:OnesCountProblemBinaryBitArraySolution, 
            optimizer: Algorithm)->OnesCountProblemBinaryBitArraySolution:
        """
        Executes "first improvement" variant of the local search procedure 
        
        :param int k: int parameter for VNS
        :param `OnesCountProblem` problem: problem that is solved
        :param `OnesCountProblemBinaryBitArraySolution` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        :return: result of the local search procedure 
        :rtype: OnesCountProblemBinaryBitArraySolution
        """
        if optimizer.finish_control.check_evaluations and optimizer.evaluation > optimizer.finish_control.evaluations_max:
            return solution
        if k < 1 or k > problem.dimension:
            return solution
        best_qos:QualityOfSolution = QualityOfSolution(solution.objective_value, solution.objective_values,
                                        solution.fitness_value, solution.fitness_values, solution.is_feasible)
        # initialize indexes
        indexes:ComplexCounterUniformAscending = ComplexCounterUniformAscending(k, problem.dimension)
        in_loop:bool = indexes.reset()
        while in_loop:
            # collect positions for inversion from indexes
            positions:list[int] = indexes.current_state()
            # invert and compare, switch and exit if new is better
            solution.representation.invert(positions) 
            optimizer.evaluation += 1
            if optimizer.finish_control.check_evaluations and optimizer.evaluation > optimizer.finish_control.evaluations_max:
                return solution
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            new_qos:QualityOfSolution = solution.calculate_quality(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            if QualityOfSolution.is_first_fitness_better(new_qos, best_qos, problem.is_minimization):
                solution.objective_value = new_qos.objective_value
                solution.fitness_value = new_qos.fitness_value
                solution.is_feasible = new_qos.is_feasible
                return solution
            solution.representation.invert(positions)
            # increment indexes and set in_loop accordingly
            in_loop = indexes.progress()
        return solution

    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the vns support structure

        :param delimiter: delimiter between fields
        :type delimiter: str
        :param indentation: level of indentation
        :type indentation: int, optional, default value 0
        :param indentation_symbol: indentation symbol
        :type indentation_symbol: str, optional, default value ''
        :param group_start: group start string 
        :type group_start: str, optional, default value '{'
        :param group_end: group end string 
        :type group_end: str, optional, default value '}'
        :return: string representation of vns support instance
        :rtype: str
        """        
        return 'OnesCountProblemBinaryBitArraySolutionVnsSupport'

    def __str__(self)->str:
        """
        String representation of the vns support instance

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self)->str:
        """
        Representation of the vns support instance

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('\n')


    def __format__(self, spec:str)->str:
        """
        Formatted the vns support instance

        :param str spec: format specification
        :return: formatted vns support instance
        :rtype: str
        """
        return self.string_rep('|')


