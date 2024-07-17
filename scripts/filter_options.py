from scripts.map_system_parameters import OBJECTIVE_PARAMETER_DICT

TIMEHORIZONS_OF_INTEREST = [20, 60, 100]

# ROBUSTNESS_METRICS_LIST = ['5%', '50%', '95%', 'average']  # 5% means that only in 5% of cases a performance is exceeded
ROBUSTNESS_METRICS_LIST = ['average']  # 5% means that only in 5% of cases a performance is exceeded

SCENARIO_OPTIONS = [['D', 'G', 'Wp'], ['D'], ['G'], ['Wp'],['D', 'G'], ['D', 'Wp'], ['G', 'Wp']]


NORMALIZATION_BENCHMARKS = {OBJECTIVE_PARAMETER_DICT['cost_d_a']: {'20': 25, '60': 100, '100': 180},
                            OBJECTIVE_PARAMETER_DICT['cost_f_u']: {'20': 330, '60': 550, '100': 720},
                            OBJECTIVE_PARAMETER_DICT['cost_d_s']: {'20': 1300, '60': 2150, '100': 3300},
                            OBJECTIVE_PARAMETER_DICT['cost_f_a']: {'20': 150, '60': 350, '100': 500}
                            }


for timehorizon in TIMEHORIZONS_OF_INTEREST:
    NORMALIZATION_BENCHMARKS[timehorizon] = {}
    for performance in ROBUSTNESS_METRICS_LIST:
        NORMALIZATION_BENCHMARKS[timehorizon][performance] = {}


