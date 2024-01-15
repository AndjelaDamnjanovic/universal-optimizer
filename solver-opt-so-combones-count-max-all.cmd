cd opt/single_objective/comb/ones_count_max_problem
@echo -----------
python solver.py -h
@echo -----------
python solver.py idle -h
@echo -----------
python solver.py variable_neighborhood_search -h
@echo -----------
python solver.py variable_neighborhood_search --writeToOutputFile True --outputFilePath outputs/dimension_10.csv --inputFilePath inputs/dimension_10.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --solutionEvaluationCacheIsUsed False --solutionDistanceCalculationCacheIsUsed False  --additionalStatisticsIsActive False --additionalStatisticsKeep none  --additionalStatisticsMaxLocalOptimaCount 5 --kMin 1 --kMax 3 --localSearchType localSearchBestImprovement --solutionType int
@echo -----------
python solver.py variable_neighborhood_search --writeToOutputFile True --outputFilePath outputs/dimension_10.csv --inputFilePath inputs/dimension_10.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --randomSeed 0 --solutionEvaluationCacheIsUsed False --solutionDistanceCalculationCacheIsUsed False  --additionalStatisticsIsActive False --additionalStatisticsKeep none --additionalStatisticsMaxLocalOptimaCount 5  --kMin 1 --kMax 3 --localSearchType localSearchBestImprovement --solutionType int
@echo -----------
python solver.py variable_neighborhood_search --writeToOutputFile True --outputFilePath outputs/dimension_10.csv --inputFilePath inputs/dimension_10.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --solutionEvaluationCacheIsUsed False --solutionDistanceCalculationCacheIsUsed False  --additionalStatisticsIsActive False --additionalStatisticsKeep none --additionalStatisticsMaxLocalOptimaCount 5  --kMin 1 --kMax 3 --localSearchType localSearchBestImprovement --solutionType BitArray
@echo -----------
python solver.py variable_neighborhood_search --writeToOutputFile True --outputFilePath outputs/dimension_10.csv --inputFilePath inputs/dimension_10.txt --inputFormat txt --finishCriteria evaluations --finishEvaluationsMax 500 --finishIterationsMax 0 --finishSecondsMax 0 --randomSeed 0 --solutionEvaluationCacheIsUsed False --solutionDistanceCalculationCacheIsUsed False  --additionalStatisticsIsActive False --additionalStatisticsKeep none --additionalStatisticsMaxLocalOptimaCount 5 --kMin 1 --kMax 3 --localSearchType localSearchFirstImprovement --solutionType BitArray
@echo -----------
python solver.py total_enumeration -h
@echo -----------
python solver.py total_enumeration --writeToOutputFile True --outputFilePath outputs/dimension_5.csv --inputFilePath inputs/dimension_5.txt --inputFormat txt --solutionType BitArray
