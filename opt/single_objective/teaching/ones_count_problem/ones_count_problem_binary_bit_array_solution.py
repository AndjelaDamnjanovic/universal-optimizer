""" 
..  _py_ones_count_problem_bit_array_solution:

The :mod:`~opt.single_objective.teaching.ones_count_problem.ones_count_problem_binary_bit_array_solution` contains class :class:`~opt.single_objective.teaching.ones_count_problem.ones_count_problem_binary_bit_array_solution.OnesCountProblemBinaryBitArraySolution`, that represents solution of the :ref:`Problem_Max_Ones`, where `BitArray` representation of the problem has been used.
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

from uo.target_problem.target_problem import TargetProblem
from uo.target_solution.target_solution import QualityOfSolution
from uo.target_solution.target_solution import TargetSolution

from uo.utils.logger import logger

class OnesCountProblemBinaryBitArraySolution(TargetSolution[BitArray,str]):
    
    def __init__(self, random_seed:int=None, 
            evaluation_cache_is_used:bool=False, 
            evaluation_cache_max_size:int=0,
            distance_calculation_cache_is_used:bool=False,
            distance_calculation_cache_max_size:int=0)->None:
        """
        Create new `OnesCountProblemBinaryBitArraySolution` instance
        """
        super().__init__("OnesCountProblemBinaryBitArraySolution", random_seed=random_seed, fitness_value=None, fitness_values=None,
                objective_value=None, objective_values=None, is_feasible=False, evaluation_cache_is_used=evaluation_cache_is_used,
                evaluation_cache_max_size=evaluation_cache_max_size,
                distance_calculation_cache_is_used=distance_calculation_cache_is_used,
                distance_calculation_cache_max_size=distance_calculation_cache_max_size)

    def __copy__(self):
        """
        Internal copy of the `OnesCountProblemBinaryBitArraySolution`

        :return: new `OnesCountProblemBinaryBitArraySolution` instance with the same properties
        :rtype: OnesCountProblemBinaryBitArraySolution
        """
        sol = super().__copy__()
        if self.representation is not None:
            sol.representation = BitArray(bin=self.representation.bin)
        else:
            sol.representation = None
        return sol

    def copy(self):
        """
        Copy the `OnesCountProblemBinaryBitArraySolution`
        
        :return: new `OnesCountProblemBinaryBitArraySolution` instance with the same properties
        :rtype: `OnesCountProblemBinaryBitArraySolution`
        """
        return self.__copy__()
        
    def argument(self, representation:BitArray)->str:
        """
        Argument of the target solution

        :param representation: internal representation of the solution
        :type representation: `BitArray`
        :return: solution code
        :rtype: str 
        """
        return representation.bin

    def init_random(self, problem:TargetProblem)->None:
        """
        Random initialization of the solution

        :param `TargetProblem` problem: problem which is solved by solution
        """
        #logger.debug('Solution: ' + str(self))
        if problem.dimension is None:
            raise ValueError('Can not randomly initialize solution without its dimension.')
        if problem.dimension <0:
            raise ValueError('Can not randomly initialize solution with negative dimension.')
        self.representation = BitArray(problem.dimension)
        for i in range(problem.dimension):
            if random() > 0.5:
                self.representation[i] = True

    def init_from(self, representation:BitArray, problem:TargetProblem)->None:
        """
        Initialization of the solution, by setting its native representation 

        :param BitArray representation: representation that will be ste to solution
        :param `TargetProblem` problem: problem which is solved by solution
        """
        if not isinstance(representation, BitArray):
            raise TypeError('Representation have to be BitArray.')
        if len(representation) == 0:
            raise ValueError('Representation must have positive length.')
        self.representation = BitArray(bin=representation.bin)

    def calculate_quality_directly(self, representation:BitArray, 
            problem:TargetProblem)->QualityOfSolution:
        """
        Fitness calculation of the max ones binary BitArray solution

        :param BitArray representation: native representation of solution whose fitness is calculated
        :param TargetProblem problem: problem that is solved
        :return: objective value, fitness value and feasibility of the solution instance  
        :rtype: `QualityOfSolution`
        """
        ones_count = representation.count(True)
        return QualityOfSolution(ones_count, None, ones_count, None, True)

    def native_representation(self, representation_str:str)->BitArray:
        """
        Obtain `BitArray` representation from string representation of the BitArray binary solution of the Max Ones problem 

        :param str representation_str: solution's representation as string
        :return: solution's representation as BitArray
        :rtype: `BitArray`
        """
        if not isinstance(representation_str, str):
            raise TypeError('Representation argument have to be string.')
        ret:BitArray = BitArray(bin=representation_str)
        return ret

    def representation_distance_directly(self, solution_code_1:str, solution_code_2:str)->float:
        """
        Calculating distance between two solutions determined by its code

        :param str solution_code_1: solution code for the first solution
        :param str solution_code_2: solution code for the second solution
        :return: distance between two solutions represented by its code
        :rtype: float
        """
        rep_1:BitArray = self.native_representation(solution_code_1)
        rep_2:BitArray = self.native_representation(solution_code_2)
        result = (rep_1 ^ rep_2).count(True)
        return result 

    def string_rep(self, delimiter:str='\n', indentation:int=0, indentation_symbol:str='   ', 
            group_start:str='{', group_end:str='}',)->str:
        """
        String representation of the solution instance

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
        :return: string representation of instance that controls output
        :rtype: str
        """        
        s = delimiter
        for i in range(0, indentation):
            s += indentation_symbol  
        s += group_start
        s += super().string_rep(delimiter, indentation, indentation_symbol, '', '')
        s += delimiter
        s += delimiter
        for i in range(0, indentation):
            s += indentation_symbol  
        s += 'string_representation()=' + str(self.string_representation())
        s += delimiter
        for i in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s

    def __str__(self)->str:
        """
        String representation of the solution instance

        :return: string representation of the solution instance
        :rtype: str
        """
        return self.string_rep('\n', 0, '   ', '{', '}')

    def __repr__(self)->str:
        """
        Representation of the solution instance

        :return: string representation of the solution instance
        :rtype: str
        """
        return self.string_rep('\n', 0, '   ', '{', '}')

    def __format__(self, spec:str)->str:
        """
        Formatted the solution instance

        :param str spec: format specification
        :return: formatted solution instance
        :rtype: str
        """
        return self.string_rep('\n', 0, '   ', '{', '}')

