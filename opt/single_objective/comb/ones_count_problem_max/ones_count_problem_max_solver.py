""" 
The :mod:`opt.single_objective.teaching.ones_count_problem.solver` contains programming code that optimize :ref:`Max Ones Problem` with various optimization techniques.
"""
import sys


from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from dataclasses import dataclass

from random import randrange
from random import seed
from datetime import datetime

from bitstring import BitArray

import xarray as xr
from linopy import Model

from uo.utils.files import ensure_dir 
from uo.utils.logger import logger

from uo.target_problem.target_problem import TargetProblem
from uo.target_solution.target_solution import TargetSolution

from uo.algorithm.output_control import OutputControl
from uo.algorithm.optimizer import Optimizer
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl

from uo.algorithm.exact.total_enumeration.te_optimizer import TeOptimizerConstructionParameters
from uo.algorithm.exact.total_enumeration.te_optimizer import TeOptimizer
from uo.algorithm.exact.total_enumeration.problem_solution_te_support import ProblemSolutionTeSupport

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizerConstructionParameters
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizer
from uo.algorithm.metaheuristic.variable_neighborhood_search.problem_solution_vns_support import \
        ProblemSolutionVnsSupport

from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_ilp_linopy import \
        OnesCountProblemMaxIntegerLinearProgrammingSolverConstructionParameters
from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_ilp_linopy import \
        OnesCountProblemMaxIntegerLinearProgrammingSolver

from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max import OnesCountProblemMax

from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_binary_int_solution import \
        OnesCountProblemMaxBinaryIntSolution
from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_binary_int_solution_vns_support import \
        OnesCountProblemMaxBinaryIntSolutionVnsSupport

from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_binary_bit_array_solution import \
        OnesCountProblemMaxBinaryBitArraySolution
from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_binary_bit_array_solution_vns_support import \
        OnesCountProblemMaxBinaryBitArraySolutionVnsSupport
from opt.single_objective.comb.ones_count_problem_max.ones_count_problem_max_binary_bit_array_solution_te_support import\
        OnesCountProblemMaxBinaryBitArraySolutionTeSupport

@dataclass
class MaxOneProblemSolverConstructionParameters:
        """
        Instance of the class :class:`MaxOneProblemSolverConstructionParameters` represents constructor parameters for max ones problem solver.
        """
        method: str = None
        finish_control: FinishControl = None
        output_control: OutputControl = None
        target_problem: TargetProblem = None
        solution_template: TargetSolution = None
        vns_problem_solution_support: ProblemSolutionVnsSupport = None
        vns_random_seed: int = None
        vns_additional_statistics_control: AdditionalStatisticsControl = None
        vns_k_min: int = None
        vns_k_max: int = None
        vns_local_search_type: str = None
        te_problem_solution_support:ProblemSolutionTeSupport = None

class OnesCountProblemMaxSolver:
    """
    Instance of the class :class:`OnesCountProblemMaxSolver` any of the developed solvers Ones Count Problem.
    """
    def __init__(self, method:str=None,
            finish_control:FinishControl = None,
            output_control:OutputControl = None,
            target_problem:TargetProblem = None,
            solution_template:TargetSolution = None,
            vns_problem_solution_support:ProblemSolutionVnsSupport = None,
            vns_random_seed:int = None,
            vns_additional_statistics_control:AdditionalStatisticsControl = None,
            vns_k_min:int = None,
            vns_k_max:int = None,
            vns_local_search_type:str = None,
            te_problem_solution_support:ProblemSolutionTeSupport = None
    )->None:
        """
        Create new `OnesCountProblemMaxSolver` instance

        :param str method: method used for solving the Max Ones Problem 
        :param FinishControl finish_control: controls finish criteria
        :param output_control:OutputControl = controls output
        :param TargetProblem target_problem: problem that is solved
        :param TargetSolution solution_template: initial solution
        :param ProblemSolutionVnsSupport vns_problem_solution_support: Specific VNS support
        :param int vns_random_seed: random seed
        :param AdditionalStatisticsControl vns_additional_statistics_control: additional statistics control
        :param int vns_k_min: VNS parameter k_min
        :param int vns_k_max: VNS parameter k_max
        :param str vns_local_search_type: type of the local search        
        """
        if not isinstance(method, str):
                raise TypeError('Parameter \'method\' must be \'str\'.')
        self.__optimizer:Optimizer = None
        if method == 'variable_neighborhood_search':
            if not isinstance(finish_control, FinishControl):
                    raise TypeError('Parameter \'finish_control\' must be \'FinishControl\'.')
            if not isinstance(output_control, OutputControl):
                    raise TypeError('Parameter \'output_control\' must be \'OutputControl\'.')
            if not isinstance(target_problem, TargetProblem):
                    raise TypeError('Parameter \'target_problem\' must be \'TargetProblem\'.')
            if not isinstance(solution_template, TargetSolution):
                    raise TypeError('Parameter \'solution_template\' must be \'TargetSolution\'.')
            if not isinstance(vns_problem_solution_support, ProblemSolutionVnsSupport):
                    raise TypeError('Parameter \'vns_problem_solution_support\' must be \'ProblemSolutionVnsSupport\'.')
            if not isinstance(vns_random_seed, int):
                    raise TypeError('Parameter \'vns_random_seed\' must be \'int\'.')
            if not isinstance(vns_additional_statistics_control, AdditionalStatisticsControl):
                    raise TypeError('Parameter \'vns_additional_statistics_control\' must be \'AdditionalStatisticsControl\'.')
            if not isinstance(vns_k_min, int):
                    raise TypeError('Parameter \'vns_k_min\' must be \'int\'.')
            if not isinstance(vns_k_max, int):
                    raise TypeError('Parameter \'vns_k_max\' must be \'int\'.')
            if not isinstance(vns_local_search_type, str):
                    raise TypeError('Parameter \'vns_local_search_type\' must be \'str\'.')
            self.__optimizer = VnsOptimizer(
                    finish_control= finish_control,
                    output_control= output_control,
                    target_problem= target_problem,
                    solution_template= solution_template,
                    problem_solution_vns_support= vns_problem_solution_support,
                    random_seed= vns_random_seed, 
                    additional_statistics_control= vns_additional_statistics_control,
                    k_min= vns_k_min,
                    k_max= vns_k_max,
                    local_search_type= vns_local_search_type)
        elif method == 'total_enumeration':
            if not isinstance(output_control, OutputControl):
                    raise TypeError('Parameter \'output_control\' must be \'OutputControl\'.')
            if not isinstance(target_problem, TargetProblem):
                    raise TypeError('Parameter \'target_problem\' must be \'TargetProblem\'.')
            if not isinstance(solution_template, TargetSolution):
                    raise TypeError('Parameter \'solution_template\' must be \'TargetSolution\'.')
            if not isinstance(te_problem_solution_support, ProblemSolutionTeSupport):
                    raise TypeError('Parameter \'te_problem_solution_support\' must be \'ProblemSolutionTeSupport\'.')
            self.__optimizer = TeOptimizer(
                    output_control = output_control,
                    target_problem= target_problem,
                    solution_template= solution_template,
                    problem_solution_te_support= te_problem_solution_support
            )
        elif method == 'integer_linear_programming':
            if not isinstance(output_control, OutputControl):
                    raise TypeError('Parameter \'output_control\' must be \'OutputControl\'.')
            if not isinstance(target_problem, TargetProblem):
                    raise TypeError('Parameter \'target_problem\' must be \'TargetProblem\'.')
            self.__optimizer:Optimizer = OnesCountProblemMaxIntegerLinearProgrammingSolver(
                output_control = output_control,
                problem = target_problem
            )
        else:
            raise ValueError("Invalid optimization method {} - should be one of: '{}', '{}', '{}'.".format(method,
                    'variable_neighborhood_search', 'total_enumeration', 'integer_linear_programming'))


    @classmethod
    def from_construction_tuple(cls, construction_params:MaxOneProblemSolverConstructionParameters=None):
        """
        Additional constructor. Create new `OnesCountProblemMaxSolver` instance from construction parameters

        :param `MaxOneProblemSolverConstructionParameters` construction_params: parameters for construction 
        """
        return cls(
            method = construction_params.method,
            finish_control = construction_params.finish_control,
            output_control = construction_params.output_control,
            target_problem = construction_params.target_problem,
            solution_template = construction_params.solution_template,
            vns_problem_solution_support = construction_params.vns_problem_solution_support,
            vns_random_seed = construction_params.vns_random_seed, 
            vns_additional_statistics_control = construction_params.vns_additional_statistics_control,
            vns_k_min = construction_params.vns_k_min,
            vns_k_max = construction_params.vns_k_max,
            vns_local_search_type = construction_params.vns_local_search_type,
            te_problem_solution_support= construction_params.te_problem_solution_support
        )

    @classmethod
    def from_variable_neighborhood_search(cls, vns_construction_params:VnsOptimizerConstructionParameters=None):
        """
        Additional constructor. Create new `OnesCountProblemMaxSolver` instance when solving method is `Variable Neighborhood Search`

        :param VnsOptimizerConstructionParameters vns_construction_params: construction parameters 
        """
        params:MaxOneProblemSolverConstructionParameters = MaxOneProblemSolverConstructionParameters()
        params.method:str = 'variable_neighborhood_search'
        params.finish_control:FinishControl = vns_construction_params.finish_control
        params.output_control:OutputControl = vns_construction_params.output_control
        params.target_problem:TargetProblem = vns_construction_params.target_problem
        params.solution_template:TargetSolution = vns_construction_params.solution_template
        params.vns_problem_solution_support:ProblemSolutionVnsSupport = \
                vns_construction_params.problem_solution_vns_support
        params.vns_random_seed:int = vns_construction_params.random_seed
        params.vns_additional_statistics_control:AdditionalStatisticsControl = \
                vns_construction_params.additional_statistics_control
        params.vns_k_min:int = vns_construction_params.k_min
        params.vns_k_max:int = vns_construction_params.k_max
        params.vns_local_search_type:str = vns_construction_params.local_search_type        
        return cls.from_construction_tuple(params)

    @classmethod
    def from_total_enumeration(cls, te_construction_params:TeOptimizerConstructionParameters=None):
        """
        Additional constructor. Create new `OnesCountProblemMaxSolver` instance when solving method is `Total Enumeration`

        :param TeOptimizerConstructionParameters te_construction_params: construction parameters 
        """
        params:MaxOneProblemSolverConstructionParameters = MaxOneProblemSolverConstructionParameters()
        params.method = 'total_enumeration'
        params.output_control = te_construction_params.output_control
        params.target_problem = te_construction_params.target_problem
        params.solution_template= te_construction_params.solution_template
        params.te_problem_solution_support= te_construction_params.problem_solution_te_support
        return cls.from_construction_tuple(params)

    @classmethod
    def from_integer_linear_programming(cls, ilp_construction_params:\
            OnesCountProblemMaxIntegerLinearProgrammingSolverConstructionParameters=None):
        """
        Additional constructor. Create new `OnesCountProblemMaxSolver` instance when solving method is `Integer Linear Programming`

        :param `OnesCountProblemMaxIntegerLinearProgrammingSolverConstructionParameters` ilp_construction_params: construction parameters 
        """
        params:MaxOneProblemSolverConstructionParameters = MaxOneProblemSolverConstructionParameters()
        params.method = 'integer_linear_programming'
        params.output_control = ilp_construction_params.output_control
        params.target_problem = ilp_construction_params.target_problem
        return cls.from_construction_tuple(params)

    @property
    def opt(self)->Optimizer:
        """
        Property getter for the optimizer used for solving

        :return: optimizer
        :rtype: `Optimizer`
        """
        return self.__optimizer

