cd opt/single_objective/trivial/max_ones_problem
@echo -----------
solver.py -h
@echo -----------
solver.py idle -h
@echo -----------
solver.py variable_neighborhood_search -h
@echo -----------
solver.py variable_neighborhood_search maximization --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --evaluationCacheIsUsed False --calculationSolutionDistanceCacheIsUsed False --keepAllSolutionCodes False  --kMin 1 --kMax 3 --maxLocalOptima 5 --localSearchType local_search_best_improvement --solutionType int
@echo -----------
solver.py variable_neighborhood_search maximization --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --randomSeed 0 --evaluationCacheIsUsed False --calculationSolutionDistanceCacheIsUsed False --keepAllSolutionCodes False  --kMin 1 --kMax 3 --maxLocalOptima 5 --localSearchType local_search_first_improvement --solutionType int
@echo -----------
solver.py variable_neighborhood_search maximization --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --evaluationCacheIsUsed False --calculationSolutionDistanceCacheIsUsed False --keepAllSolutionCodes False  --kMin 1 --kMax 3 --maxLocalOptima 5 --localSearchType local_search_best_improvement --solutionType BitArray
@echo -----------
solver.py variable_neighborhood_search maximization --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --evaluationCacheIsUsed False --calculationSolutionDistanceCacheIsUsed False --keepAllSolutionCodes False  --kMin 1 --kMax 3 --maxLocalOptima 5 --localSearchType local_search_first_improvement --solutionType BitArray
@echo -----------
solver.py total_enumeration -h
@echo -----------
solver.py total_enumeration maximization --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --solutionType BitArray
