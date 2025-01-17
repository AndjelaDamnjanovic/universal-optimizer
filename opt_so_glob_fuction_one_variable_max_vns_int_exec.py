from copy import deepcopy
from random import randint
from random import choice

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_standard_int import \
        VnsShakingSupportStandardInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_bi_int import \
        VnsLocalSearchSupportStandardBestImprovementInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizerConstructionParameters
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizer

from opt.single_objective.glob.function_one_variable_max_problem.function_one_variable_max_problem import \
                FunctionOneVariableMaxProblemMax
from opt.single_objective.glob.function_one_variable_max_problem.function_one_variable_max_problem_int_solution \
                import FunctionOneVariableMaxProblemIntSolution

def main():
        problem_to_solve:FunctionOneVariableMaxProblemMax = FunctionOneVariableMaxProblemMax.from_input_file(
                input_file_path='./opt/single_objective/glob/function_one_variable_max_problem/inputs/(7-x2)[-3,3].txt',
                input_format='txt')
        print('Problem: {}'.format(problem_to_solve))            
        solution:FunctionOneVariableMaxProblemIntSolution = FunctionOneVariableMaxProblemIntSolution(
                domain_from=problem_to_solve.domain_low, domain_to=problem_to_solve.domain_high, 
                number_of_intervals=6000, random_seed=43434343)
        solution.init_random(problem=problem_to_solve)
        solution.evaluate(problem_to_solve)           
        print('Solution: {}'.format(solution))
        finish:FinishControl = FinishControl(criteria='evaluations & seconds', evaluations_max=5000, seconds_max=10)
        repr_length:int = 32
        vns_shaking_support:VnsShakingSupportStandardInt[str] = \
                VnsShakingSupportStandardInt[str](repr_length)
        vns_ls_support:VnsLocalSearchSupportStandardBestImprovementInt[str] = \
                VnsLocalSearchSupportStandardBestImprovementInt[str](repr_length)
        vns_construction_params:VnsOptimizerConstructionParameters = VnsOptimizerConstructionParameters()
        vns_construction_params.problem = problem_to_solve
        vns_construction_params.solution_template = solution
        vns_construction_params.vns_shaking_support = vns_shaking_support
        vns_construction_params.vns_ls_support = vns_ls_support
        vns_construction_params.finish_control = finish
        vns_construction_params.random_seed = 43434343
        vns_construction_params.k_min = 1
        vns_construction_params.k_max = 3
        optimizer:VnsOptimizer = VnsOptimizer.from_construction_tuple(vns_construction_params)
        bs = optimizer.optimize()
        print('Best solution representation: {}'.format(bs.representation))            
        print('Best solution code: {}'.format(bs.string_representation()))            
        print('Best solution objective:  {}'.format(bs.objective_value))
        print('Best solution fitness: {}'.format(bs.fitness_value))
        print('Number of iterations: {}'.format(optimizer.iteration))            
        print('Number of evaluations: {}'.format(optimizer.evaluation))            

if __name__ == '__main__':
        main()