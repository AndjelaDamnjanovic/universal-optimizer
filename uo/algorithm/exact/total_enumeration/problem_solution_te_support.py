""" 
The :mod:`~uo.algorithm.exact.total_enumeration.problem_solution_te_support` module describes the class :class:`~uo.algorithm.exact.total_enumeration.problem_solution_te_support.ProblemSolutionTeSupport`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic
from typing import Generic

from uo.target_problem.target_problem import TargetProblem
from uo.target_solution.target_solution import TargetSolution
from uo.algorithm.algorithm import Algorithm

R_co = TypeVar("R_co", covariant=True) 

class ProblemSolutionTeSupport(Generic[R_co], metaclass=ABCMeta):
    
    @abstractmethod
    def reset(self, problem:TargetProblem, solution:TargetSolution[R_co], optimizer:Algorithm)->None:
        """
        Resets internal counter of the total enumerator, so process will start over. Internal state of the solution 
        will be set to reflect reset operation. 

        :param `TargetProblem` problem: problem that is solved
        :param `TargetSolution[R_co]` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        """        
        raise NotImplementedError

    @abstractmethod
    def progress(self, problem:TargetProblem, solution:TargetSolution[R_co], optimizer:Algorithm)->None:
        """
        Progress internal counter of the total enumerator, so next configuration will be taken into consideration. 
        Internal state of the solution will be set to reflect progress operation.  

        :param `TargetProblem` problem: problem that is solved
        :param `TargetSolution[R_co]` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        """        
        raise NotImplementedError

    @abstractmethod
    def can_progress(self, problem:TargetProblem, solution:TargetSolution[R_co], optimizer:Algorithm)->bool:
        """
        Check if total enumeration process is not at end.  

        :param `TargetProblem` problem: problem that is solved
        :param `TargetSolution[R_co]` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        :return: indicator if total enumeration process is not at end 
        :rtype: bool
        """        
        raise NotImplementedError

    @abstractmethod
    def overall_number_of_evaluations(self, problem:TargetProblem, solution:TargetSolution[R_co], optimizer:Algorithm)->int:
        """
        Returns overall number of evaluations required for finishing total enumeration process.  

        :param `TargetProblem` problem: problem that is solved
        :param `TargetSolution[R_co]` solution: solution used for the problem that is solved
        :param `Algorithm` optimizer: optimizer that is executed
        :return: overall number of evaluations required for finishing total enumeration process
        :rtype: int
        """        
        raise NotImplementedError
