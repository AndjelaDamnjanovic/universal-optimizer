""" 
The :mod:`opt.single_objective.comb.ones_count_max_problem.solver` contains programming code that optimize :ref:`Max Ones<Problem_Ones_Count_Max>` Problem with various optimization techniques.
"""
import sys

from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from random import randrange
from random import seed
from datetime import datetime

from uo.utils.files import ensure_dir 
from uo.utils.logger import logger

from bitstring import BitArray

import xarray as xr
from linopy import Model

from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl

from uo.algorithm.metaheuristic.genetic_algorithm.selection_roulette import SelectionRoulette
from uo.algorithm.metaheuristic.genetic_algorithm.ga_crossover_support_one_point_rep_bit_array import \
                GaCrossoverSupportOnePointRepresentationBitArray
from uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support_one_point_rep_bit_array import \
                GaMutationSupportOnePointRepresentationBitArray
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer import GaOptimizerConstructionParameters
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer import GaOptimizer

from uo.algorithm.exact.total_enumeration.te_operations_support_rep_bit_array import\
        TeOperationsSupportRepresentationBitArray
from uo.algorithm.exact.total_enumeration.te_optimizer import TeOptimizerConstructionParameters

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_rep_bit_array import \
        VnsShakingSupportRepresentationBitArray
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_rep_bit_array import \
        VnsLocalSearchSupportRepresentationBitArray
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_rep_int import \
        VnsShakingSupportRepresentationInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_rep_int import \
        VnsLocalSearchSupportRepresentationInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizerConstructionParameters
from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_ilp_linopy import \
        OnesCountMaxProblemIntegerLinearProgrammingSolverConstructionParameters

from opt.single_objective.comb.ones_count_max_problem.command_line import default_parameters_cl
from opt.single_objective.comb.ones_count_max_problem.command_line import parse_arguments

from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem import OnesCountMaxProblem
from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_int_solution import \
        OnesCountMaxProblemIntSolution
from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_bit_array_solution import \
        OnesCountMaxProblemBitArraySolution
from opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_solver import OnesCountMaxProblemSolver

""" 
Solver.

Which solver will be executed depends of command-line parameter algorithm.
"""

def main():
    """ 
    This function executes solver.

    Which solver will be executed depends of command-line parameter algorithm.
    """
    try:
        logger.debug('Solver started.')    
        parameters = default_parameters_cl
        read_parameters_cl = parse_arguments()
        for param_key_value in read_parameters_cl._get_kwargs():
            key:str = param_key_value[0]
            val = param_key_value[1]
            logger.debug('key:{} value:{}'.format(key, val))
            if key is not None and val is not None:
                parameters[key] = val
        logger.debug('Execution parameters: '+ str(parameters))
        # write to output file setup
        if parameters['writeToOutputFile'] is None:
            write_to_output_file:bool = False
        else:
            write_to_output_file:bool = bool(parameters['writeToOutputFile'])
        # output file setup
        if write_to_output_file:
            if parameters['outputFileNameAppendTimeStamp'] is None:
                should_add_timestamp_to_file_name:bool = False
            else:
                should_add_timestamp_to_file_name:bool = bool(parameters['outputFileNameAppendTimeStamp'])
            if parameters['outputFilePath'] is not None and  parameters['outputFilePath'] != '':
                output_file_path_parts:list[str] = parameters['outputFilePath'].split('/')
            else:
                output_file_path_parts:list[str] = ['outputs', 'out']
            output_file_name_ext:str = output_file_path_parts[-1]
            output_file_name_parts:list[str] = output_file_name_ext.split('.')
            if len(output_file_name_parts) > 1:
                output_file_ext:str = output_file_name_parts[-1]
                output_file_name_parts.pop()
                output_file_name = '.'.join(output_file_name_parts)
            else:
                output_file_ext = 'txt'
                output_file_name = output_file_name_parts[0]
            dt = datetime.now()
            output_file_path_parts.pop()
            output_file_dir:str =  '/'.join(output_file_path_parts)
            if should_add_timestamp_to_file_name:
                output_file_path_parts.append( output_file_name +  '-maxones-'  + parameters['algorithm'] + '-' + 
                        parameters['solutionType'] + '-' + dt.strftime("%Y-%m-%d-%H-%M-%S.%f") + '.' + output_file_ext)
            else:
                output_file_path_parts.append( output_file_name +  '-maxones-' +  parameters['algorithm'] + '-' + 
                        parameters['solutionType'] + '.' + output_file_ext)
            output_file_path:str = '/'.join(output_file_path_parts)
            logger.debug('Output file path: ' + str(output_file_path))
            ensure_dir(output_file_dir)
            output_file = open(output_file_path, "w", encoding="utf-8")
        # output control setup
        if write_to_output_file:    
            output_fields:str = parameters['outputFields']
            output_moments:str = parameters['outputMoments']
            output_control:OutputControl = OutputControl(write_to_output=True,
                    output_file=output_file,
                    fields=output_fields,
                    moments=output_moments)
        else:
            output_control:OutputControl = OutputControl(write_to_output=False)
        # input file setup
        input_file_path:str = parameters['inputFilePath']
        input_format:str = parameters['inputFormat']
        # random seed setup
        if( int(parameters['randomSeed']) > 0 ):
            r_seed:int = int(parameters['randomSeed'])
            logger.info('RandomSeed is predefined. Predefined seed value:  %d' % r_seed)
            if write_to_output_file:
                output_file.write('# RandomSeed is predefined. Predefined seed value:  %d\n' % r_seed)
            seed(r_seed)
        else:
            r_seed = randrange(sys.maxsize) #NOSONAR
            logger.info('RandomSeed is not predefined. Generated seed value:  %d' % r_seed)
            if write_to_output_file:
                output_file.write("# RandomSeed is not predefined. Generated seed value:  %d\n" % r_seed)
            seed(r_seed)
        # finishing criteria setup
        finish_criteria:str = parameters['finishCriteria']
        max_number_evaluations:int = parameters['finishEvaluationsMax']
        max_number_iterations:int = parameters['finishIterationsMax']
        max_time_for_execution_in_seconds = parameters['finishSecondsMax']
        finish_control:FinishControl = FinishControl(
                criteria=finish_criteria,
                evaluations_max=max_number_evaluations,
                iterations_max=max_number_iterations,
                seconds_max=max_time_for_execution_in_seconds)
        # solution evaluations and calculations cache setup
        evaluation_cache_is_used:bool = parameters['solutionEvaluationCacheIsUsed']
        evaluation_cache_max_size:int = parameters['solutionEvaluationCacheMaxSize']
        calculation_solution_distance_cache_is_used:bool = parameters['solutionDistanceCalculationCacheIsUsed']
        calculation_solution_distance_cache_max_size:int = parameters['solutionDistanceCalculationCacheMaxSize']
        # additional statistic control setup
        additional_statistics_is_active:bool =  parameters['additionalStatisticsIsActive']
        additional_statistics_keep:str =  parameters['additionalStatisticsKeep']
        max_local_optima_count = parameters['additionalStatisticsMaxLocalOptimaCount']
        additional_statistics_control:AdditionalStatisticsControl = AdditionalStatisticsControl(
                is_active=additional_statistics_is_active,
                keep=additional_statistics_keep, 
                max_local_optima_count=max_local_optima_count)
        # problem to be solved
        problem = OnesCountMaxProblem.from_input_file(input_file_path=input_file_path,input_format=input_format)
        start_time = datetime.now()
        if write_to_output_file:
            output_file.write("# {} started at: {}\n".format(parameters['algorithm'], str(start_time)) )
            output_file.write('# Execution parameters: {}\n'.format(parameters))
        # select among algorithm types
        if parameters['algorithm'] == 'variable_neighborhood_search':
            # parameters for VNS process setup
            k_min:int = parameters['kMin']
            k_max:int = parameters['kMax']
            local_search_type = parameters['localSearchType']
            # initial solution and VNS support
            solution_type:str = parameters['solutionType']
            vns_shaking_support = None
            vns_ls_support = None
            if solution_type=='BitArray':
                solution:OnesCountMaxProblemBitArraySolution = OnesCountMaxProblemBitArraySolution(
                    random_seed=r_seed)
                vns_shaking_support = VnsShakingSupportRepresentationBitArray[str]()
                vns_ls_support = VnsLocalSearchSupportRepresentationBitArray[str]()
            elif solution_type=='int':
                solution:OnesCountMaxProblemIntSolution = OnesCountMaxProblemIntSolution(r_seed)
                vns_shaking_support = VnsShakingSupportRepresentationInt[str]()
                vns_ls_support = VnsLocalSearchSupportRepresentationInt[str]()
            else:
                raise ValueError("Invalid solution/representation type is chosen.")
            # solver construction parameters
            vns_construction_params:VnsOptimizerConstructionParameters = VnsOptimizerConstructionParameters()
            vns_construction_params.output_control = output_control
            vns_construction_params.problem = problem
            vns_construction_params.solution_template = solution
            vns_construction_params.finish_control = finish_control
            vns_construction_params.random_seed = r_seed
            vns_construction_params.additional_statistics_control = additional_statistics_control
            vns_construction_params.vns_shaking_support = vns_shaking_support
            vns_construction_params.vns_ls_support = vns_ls_support
            vns_construction_params.k_min = k_min
            vns_construction_params.k_max = k_max
            vns_construction_params.local_search_type = local_search_type
            solver:OnesCountMaxProblemSolver = OnesCountMaxProblemSolver.from_variable_neighborhood_search(
                    vns_construction_params)
        elif parameters['algorithm'] == 'genetic_algorithm':
            # parameters for GA process setup
            population_size:int = 100
            elite_count:int = 5
            selection:SelectionRoulette = SelectionRoulette()
            crossover_probability:float = 0.995
            mutation_probability:float = 0.05
            # initial solution and GA support
            solution_type:str = parameters['solutionType']
            ga_crossover_support = None
            ga_mutation_support = None
            if solution_type=='BitArray':
                solution:OnesCountMaxProblemBitArraySolution = OnesCountMaxProblemBitArraySolution(
                    random_seed=r_seed)
                ga_crossover_support = GaCrossoverSupportOnePointRepresentationBitArray[str](
                    crossover_probability=crossover_probability)
                ga_mutation_support = GaMutationSupportOnePointRepresentationBitArray[str](
                    mutation_probability=mutation_probability)
            else:
                raise ValueError("Invalid solution/representation type is chosen.")
            ga_construction_params:GaOptimizerConstructionParameters = GaOptimizerConstructionParameters()
            ga_construction_params.output_control = output_control
            ga_construction_params.problem = problem
            ga_construction_params.solution_template = solution
            ga_construction_params.finish_control = finish_control
            ga_construction_params.random_seed = r_seed
            ga_construction_params.additional_statistics_control = additional_statistics_control
            ga_construction_params.ga_selection = selection
            ga_construction_params.ga_crossover_support = ga_crossover_support
            ga_construction_params.ga_mutation_support = ga_mutation_support
            ga_construction_params.population_size = population_size
            ga_construction_params.elite_count = elite_count
        elif parameters['algorithm'] == 'total_enumeration':
            # initial solution and te support
            solution_type:str = parameters['solutionType']
            te_operations_support = None
            if solution_type=='BitArray':
                solution:OnesCountMaxProblemBitArraySolution = OnesCountMaxProblemBitArraySolution(r_seed, 
                            evaluation_cache_is_used=evaluation_cache_is_used,
                            evaluation_cache_max_size=evaluation_cache_max_size,
                            distance_calculation_cache_is_used=calculation_solution_distance_cache_is_used,
                            distance_calculation_cache_max_size=calculation_solution_distance_cache_max_size)
                te_operations_support = TeOperationsSupportRepresentationBitArray[str]()
            else:
                raise ValueError("Invalid solution/representation type is chosen.")
            # solver construction parameters
            te_construction_params:TeOptimizerConstructionParameters = TeOptimizerConstructionParameters()
            te_construction_params.output_control = output_control
            te_construction_params.problem = problem
            te_construction_params.solution_template = solution
            te_construction_params.te_operations_support = te_operations_support
            solver:OnesCountMaxProblemSolver = OnesCountMaxProblemSolver.from_total_enumeration(te_construction_params)
        elif parameters['algorithm'] == 'integer_linear_programming':
            # solver construction parameters
            ilp_construction_params = OnesCountMaxProblemIntegerLinearProgrammingSolverConstructionParameters(
                    output_control=output_control,
                    problem=problem)
            solver:OnesCountMaxProblemSolver = OnesCountMaxProblemSolver.from_integer_linear_programming(
                    ilp_construction_params)
        else:
            raise ValueError('Invalid optimization algorithm is chosen.')
        bs = solver.opt.optimize()
        logger.debug('Method -{}- search finished.'.format(parameters['algorithm'])) 
        logger.info('Best solution code: {}'.format(bs.string_representation()))            
        logger.info('Best solution objective: {}, fitness: {}'.format(bs.objective_value,
                bs.fitness_value))
        logger.info('Number of iterations: {}, evaluations: {}'.format(solver.opt.iteration, 
                solver.opt.evaluation))  
        logger.info('Execution: {} - {}'.format(solver.opt.execution_started, solver.opt.execution_ended))          
        logger.debug('Solver ended.')    
        return
    except Exception as exp:
        if hasattr(exp, 'message'):
            logger.exception('Exception: %s\n' % exp.message)
        else:
            logger.exception('Exception: %s\n' % str(exp))
        
# This means that if this script is executed, then 
# main() will be executed

if __name__ == '__main__':
    main()


