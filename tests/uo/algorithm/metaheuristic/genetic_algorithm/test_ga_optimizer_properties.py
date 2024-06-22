import unittest   
import unittest.mock as mocker
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl

from uo.problem.problem import Problem
from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer import GaOptimizer
from uo.algorithm.metaheuristic.genetic_algorithm.problem_solution_ga_support import ProblemSolutionGaSupport
from uo.solution.solution_void import SolutionVoid

class TestGaOptimizerProperties(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("setUpClass TestGaOptimizerProperties\n")

    def setUp(self):
        self.output_control_stub = mocker.MagicMock(spec=OutputControl)
        type(self.output_control_stub).write_to_output = False

        self.problem_mock = mocker.MagicMock(spec=Problem)
        type(self.problem_mock).name = mocker.PropertyMock(return_value='some_problem')
        type(self.problem_mock).is_minimization = mocker.PropertyMock(return_value=True)
        type(self.problem_mock).file_path = mocker.PropertyMock(return_value='some file path')
        type(self.problem_mock).dimension = mocker.PropertyMock(return_value=42)
        self.problem_mock.copy = mocker.Mock(return_value=self.problem_mock)

        self.problem_solution_ga_support_stub = mocker.MagicMock(spec=ProblemSolutionGaSupport)
        self.problem_solution_ga_support_stub.selection_roulette = mocker.Mock(return_value="mocked stuff")
        type(self.problem_solution_ga_support_stub).copy = mocker.CallableMixin(spec="return self")        
        
        self.evaluations_max = 42
        self.iterations_max = 42
        self.seconds_max = 42
        self.finish_control_mock = mocker.MagicMock(spec=FinishControl)
        type(self.finish_control_mock).evaluations_max= mocker.PropertyMock(return_value=self.evaluations_max)
        type(self.finish_control_mock).iterations_max= mocker.PropertyMock(return_value=self.iterations_max)
        type(self.finish_control_mock).seconds_max= mocker.PropertyMock(return_value=self.seconds_max)
        self.finish_control_mock.copy = mocker.Mock(return_value=self.finish_control_mock)
        
        self.random_seed = 42
        self.mutation_probability = 0.1
        self.selection_type = 'selectionRoulette'
        self.tournament_size = 10
        self.population_size = 100
        self.elitism_size = 10

        self.additional_statistics_control = AdditionalStatisticsControl()

        self.ga_optimizer:GaOptimizer = GaOptimizer(
                output_control=self.output_control_stub,
                problem=self.problem_mock, 
                solution_template=SolutionVoid( 43, 0, 0, False),
                problem_solution_ga_support=self.problem_solution_ga_support_stub,
                finish_control=self.finish_control_mock,
                random_seed=self.random_seed,
                additional_statistics_control=self.additional_statistics_control,
                tournament_size=self.tournament_size,
                mutation_probability=self.mutation_probability,
                selection_type=self.selection_type,
                population_size=self.population_size,
                elitism_size=self.elitism_size
        )

    def test_name_should_be_ga(self):
        self.assertEqual(self.ga_optimizer.name, 'ga')

    def test_evaluations_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.finish_control.evaluations_max, self.finish_control_mock.evaluations_max)

    def test_iterations_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.finish_control.iterations_max, self.finish_control_mock.iterations_max)

    def test_random_seed_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.random_seed, self.random_seed)

    def test_seconds_max_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.finish_control.seconds_max, self.finish_control_mock.seconds_max)

    def test_tournament_size_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.tournament_size, self.tournament_size)

    def test_elitism_size_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.elitism_size, self.elitism_size)

    def test_problem_name_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.problem.name, self.problem_mock.name)

    def test_problem_is_minimization_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.problem.is_minimization, self.problem_mock.is_minimization)

    def test_problem_file_path_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.problem.file_path, self.problem_mock.file_path)

    def test_problem_dimension_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.ga_optimizer.problem.dimension, self.problem_mock.dimension)

    def test_create_with_invalid_selection_type_should_raise_value_exception_with_proper_message(self):
        with self.assertRaises(ValueError) as context:
            ga_support_stub = mocker.MagicMock(spec=ProblemSolutionGaSupport)
            type(ga_support_stub).selection_roulette = mocker.CallableMixin(spec=lambda x: x)
            type(ga_support_stub).copy = mocker.CallableMixin(spec="return self")
            self.ga_optimizer:GaOptimizer = GaOptimizer(
                output_control=self.output_control_stub,
                problem=self.problem_mock, 
                solution_template=SolutionVoid( 43, 0, 0, False),
                problem_solution_ga_support=self.problem_solution_ga_support_stub,
                finish_control=self.finish_control_mock,
                random_seed=self.random_seed,
                additional_statistics_control=self.additional_statistics_control,
                tournament_size=self.tournament_size,
                mutation_probability=self.mutation_probability,
                selection_type="xxx",
                population_size=self.population_size,
                elitism_size=self.elitism_size
            )
        self.assertEqual("Value 'xxx' for GA selection_type is not supported", context.exception.args[0])

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        print("\ntearDownClass TestGaOptimizerProperties")
    
if __name__ == '__main__':
    unittest.main()