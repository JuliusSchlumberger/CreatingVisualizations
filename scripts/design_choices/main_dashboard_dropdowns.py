from scripts.map_system_parameters import SECTOR_OBJECTIVES, OBJECTIVE_PARAMETER_DICT, AXIS_LABELS

ROH_DICT = {
    'farmer - flood': 'flood_agr',
    'farmer - drought': 'drought_agr',
    'ship company - drought': 'drought_shp',
    'municipality - flood': 'flood_urb'
}

ROH_DICT_INV = {}
for key, element in ROH_DICT.items():
    ROH_DICT_INV[element] = key

TIMEHORIZONS = {
    'next 20 years': 20,
    'next 60 years': 60,
    'next 100 years': 100
}

TIMEHORIZONS_INV = {}
for key, element in TIMEHORIZONS.items():
    TIMEHORIZONS_INV[element] = key

SCENARIOS = {
    'historic': 'D',
    '1.5 Deg': 'G',
    '4 Deg': 'Wp'
}
SCENARIOS_INV = {}
for key, element in SCENARIOS.items():
    SCENARIOS_INV[element] = key

CONFIDENCE = {
    'risk averse': '95%',
    'risk neutral': '50%',
    'risk taking': '5%'
}

# PATHWAYS_TO_HIGHLIGHT = {
#     'flood_agr': range(1,13),
#     'drought_agr': range(1,9),
#     'drought_shp': range(1,12),
#     'flood_urb': range(1,18)
# }

PATHWAYS_TO_HIGHLIGHT = {
    'flood_agr': range(1,8),
    'drought_agr': range(1,8),
    'drought_shp': range(1,8),
    'flood_urb': range(1,8)
}

WHICH_OPTIONS = {
    'best': 'best',
    'worst': 'worst'
}

WHICH_OPTIONS = {
    'Parallel Coordinates Plot': 'PCP',
    'Stacked Bar': 'StackedBar',
    'Heatmap': 'Heatmap'
}

PERFORMANCE_METRICS = {
    '5% confidence interval': '5%',
    '50% confidence interval': '50%',
    '95% confidence interval': '95%',
    'expected performance': 'average'
}

INTERACTION_VIZ = {
    'Pathways Options': 'image',
    'Pathways Performance': 'graph'
}

# SECTOR_OBJECTIVES_BUTTONS = {}
# for key in SECTOR_OBJECTIVES:
#     SECTOR_OBJECTIVES_BUTTONS[key]= {}
#     for label in SECTOR_OBJECTIVES[key]:
#         SECTOR_OBJECTIVES_BUTTONS[key][label] = key_item for key_item, value in OBJECTIVE_PARAMETER_DICT.items() if label == value

SECTOR_OBJECTIVES_BUTTONS = {
    key: {label: [key_item for key_item, value in OBJECTIVE_PARAMETER_DICT.items() if label == value]
          for label in labels}
    for key, labels in SECTOR_OBJECTIVES.items()
}

label_keys = list(AXIS_LABELS.keys())
RANGE = {
    AXIS_LABELS[label_keys[0]]: [0,800],
    AXIS_LABELS[label_keys[1]]:[0,800], # 600
    AXIS_LABELS[label_keys[2]]:[0,300],
    AXIS_LABELS[label_keys[3]]:[0,800], #800
    AXIS_LABELS[label_keys[4]]:[0,20000],
    AXIS_LABELS[label_keys[5]]:[0,1000],
    AXIS_LABELS[label_keys[6]]:[0,20000],
    AXIS_LABELS[label_keys[7]]:[0,4000],
    list(ROH_DICT.keys())[0]:[0,7],
    list(ROH_DICT.keys())[1]:[0,7], # 10
    list(ROH_DICT.keys())[2]:[0,7],
    list(ROH_DICT.keys())[3]:[0,7],
    'performance_metric': [0,1]
}

