from Paper3_v1.scripts.utilities.filter_options import NORMALIZATION_BENCHMARKS
from Paper3_v1.scripts.utilities.map_system_parameters import BENCHMARK_GROUPS

def normalize_performance(row):
    # print(row['objective_parameter'], row['Value_normal'], row['Value_benchmark'])

    if row['objective_parameter'] in BENCHMARK_GROUPS['from_baseline']:
        if round(row['Value_benchmark'],2) == 0:
            return 0
        else:
            return round(row['Value_normal'] / row['Value_benchmark'],2)
    else:
        benchmark_from_input = NORMALIZATION_BENCHMARKS[row['objective_parameter']][str(row['year'])]
        return round(row['Value_normal'] / benchmark_from_input,2)

