import pandas as pd
from scripts.main_central_path_directions import FILTER_CONDITIONS, DIRECTORY_MEASURE_LOGOS_GITHUB
from scripts.DecisionTree.DecisionTree import decision_tree

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

filter_conditions = FILTER_CONDITIONS

sectors = ['flood_agr', 'drought_agr', 'flood_urb', 'drought_shp']
input_file = 'data/stage3_portfolios_'

button_path = DIRECTORY_MEASURE_LOGOS_GITHUB + '/colorized'
for sector in sectors:
    decision_tree(f'{input_file}{sector}.txt',sector, button_path, filter_conditions[sector])