from scripts.map_system_parameters import MEASURE_NUMBERS
import pandas as pd



# Logos and Legends
DIRECTORY_MEASURE_LOGOS_GITHUB = 'https://raw.githubusercontent.com/JuliusSchlumberger/CreatingVisualizations/master/logos/'
DIRECTORY_MEASURE_LOGOS = 'data/logos/'
LEGENDS_LOCATION_GITHUB = 'https://raw.githubusercontent.com/JuliusSchlumberger/CreatingVisualizations/master/legends/'

# Input data
FILE_PATH_ALL_PATHWAYS_SECTORS = 'data/decision_trees/stage3_portfolios_'
DIRECTORY_INTERACTIONS = f'data/pathways_performance/interactions'
DIRECTORY_PATHWAYS_GENERATOR = 'data/pathways_generator'


ROH_LIST = ['flood_agr', 'drought_agr', 'flood_urb', 'drought_shp']
LIST_COLUMNS = ['climvar', 'pw_combi','objective_parameter','Value','year','scenario_of_interest']
COLUMN_TYPES = {column_name: 'float32' if column_name in ['Value', 'year'] else 'category' for column_name in LIST_COLUMNS}
MEASURE_LOGOS = {measure: f'{DIRECTORY_MEASURE_LOGOS}/{measure}.png' for measure in MEASURE_NUMBERS.keys()}
MEASURE_LOGOS_GITHUB = {measure: f'{DIRECTORY_MEASURE_LOGOS_GITHUB}/logos/{measure}.png' for measure in MEASURE_NUMBERS.keys()}

PATHWYAYS_SPECIFIER = {'flood_agr': 'f_a',
                       'drought_agr': 'd_a',
                       'flood_urb': 'f_u',
                       'drought_shp': 'd_s'}

ALL_PATHWAYS = {'flood_agr': pd.read_csv(f'{FILE_PATH_ALL_PATHWAYS_SECTORS}flood_agr.txt',
                                          names=['1', '2', '3', '4'], dtype='str'),
                'drought_agr': pd.read_csv(f'{FILE_PATH_ALL_PATHWAYS_SECTORS}drought_agr.txt',
                                         names=['1', '2', '3', '4'], dtype='str'),
                'flood_urb': pd.read_csv(f'{FILE_PATH_ALL_PATHWAYS_SECTORS}flood_urb.txt',
                                                         names=['1', '2', '3', '4'], dtype='str'),
                'drought_shp': pd.read_csv(f'{FILE_PATH_ALL_PATHWAYS_SECTORS}drought_shp.txt',
                                                         names=['1', '2', '3', '4'], dtype='str'),
                }


FILTER_CONDITIONS = {
    ROH_LIST[0]: [0, 1, 3, 5, 7, 9, 11, 13],
    ROH_LIST[1]: [0, 1, 3, 5, 6, 7, 8, 9],
    ROH_LIST[2]: [0, 1, 3, 5, 7, 9, 11, 13],
    ROH_LIST[3]: [0, 1, 2, 4, 5, 8, 9 ],
}



