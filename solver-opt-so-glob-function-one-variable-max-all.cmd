cd opt/single_objective/glob/function_one_variable_max_problem
@echo -----------
solver.py -h
@echo -----------
solver.py idle -h
@echo -----------
solver.py variable_neighborhood_search -h
@echo -----------
solver.py variable_neighborhood_search maximization --writeToOutputFile True --outputFilePath outputs/(7-x2)[-3,3].csv --inputFilePath inputs/(7-x2)[-3,3].txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --solutionEvaluationCacheIsUsed False --solutionDistanceCalculationCacheIsUsed False  --additionalStatisticsIsActive False --additionalStatisticsKeep none  --additionalStatisticsMaxLocalOptimaCount 5 --kMin 1 --kMax 3 --localSearchType localSearchBestImprovement --solutionType int --solutionNumberOfIntervals 2000

