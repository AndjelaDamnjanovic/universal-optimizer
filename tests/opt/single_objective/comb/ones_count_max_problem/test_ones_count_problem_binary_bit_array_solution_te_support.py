
import unittest
import unittest.mock as mocker

from bitstring import BitArray


from uo.algorithm.output_control import OutputControl
from uo.algorithm.exact.total_enumeration.te_operations_support_rep_bit_array import \
    TeOperationsSupportRepresentationBitArray
from uo.algorithm.algorithm_void import AlgorithmVoid

from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem import OnesCountMaxProblem
from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_bit_array_solution import OnesCountMaxProblemBitArraySolution

class TestTeOperationsSupportRepresentationBitArray(unittest.TestCase):

    # can reset the internal counter of the total enumerator and set the internal state of the solution to reflect reset operation
    def test_reset_internal_counter_and_state(self):
        result:str = '00'
        problem = OnesCountMaxProblem(dim=len(result))
        solution = OnesCountMaxProblemBitArraySolution()
        solution.init_from(BitArray(bin=result), problem)
        output_control = OutputControl(write_to_output=False)
        optimizer = AlgorithmVoid("test", output_control, problem)
        te_support = TeOperationsSupportRepresentationBitArray()
    
        te_support.reset(problem, solution, optimizer)
    
        self.assertEqual(te_support._TeOperationsSupportRepresentationBitArray__bit_array_counter.current_state(), BitArray(bin=result))
        self.assertEqual(solution.representation, BitArray(bin=result))
        self.assertEqual(optimizer.evaluation, 1)

    # can progress the internal counter of the total enumerator and set the internal state of the solution to reflect progress operation
    def test_progress_internal_counter_and_state(self):
        result:str = '10'
        problem = OnesCountMaxProblem(dim=len(result))
        solution = OnesCountMaxProblemBitArraySolution()
        solution.init_from(BitArray(bin=result), problem)
        output_control = OutputControl(write_to_output=False)
        optimizer = AlgorithmVoid("test", output_control, problem)
        te_support = TeOperationsSupportRepresentationBitArray()
    
        te_support.reset(problem, solution, optimizer)
        te_support.progress(problem, solution, optimizer)
    
        self.assertEqual(te_support._TeOperationsSupportRepresentationBitArray__bit_array_counter.current_state(), BitArray(bin=result))
        self.assertEqual(solution.representation, BitArray(bin=result))
        self.assertEqual(optimizer.evaluation, 2)

    # can check if total enumeration process is not at end
    def test_can_progress(self):
        result:str = '00000'
        problem = OnesCountMaxProblem(dim=len(result))
        solution = OnesCountMaxProblemBitArraySolution()
        solution.init_from(BitArray(bin=result), problem)
        output_control = OutputControl(write_to_output=False)
        optimizer = AlgorithmVoid("test", output_control, problem)
        te_support = TeOperationsSupportRepresentationBitArray()
    
        te_support.reset(problem, solution, optimizer)
    
        self.assertTrue(te_support.can_progress(problem, solution, optimizer))

