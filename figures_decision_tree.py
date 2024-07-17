import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import plotly.graph_objects as go
import plotly.express as px
import base64
from scripts.map_system_parameters import MEASURE_DICT, MEASURE_EXPL
from scripts.main_central_path_directions import FILTER_CONDITIONS
from scripts.design_choices.main_dashboard_design_choices import MEASURE_COLORS, MEASURE_NUMBERS
from scripts.DecisionTree.DecisionTree import decision_tree

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
#
# # Function to get and display the image
# def getImage(path, zoom=0.025):
#     return OffsetImage(plt.imread(path), zoom=zoom)
#
# def image_to_base64(path):
#     with open(path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')



filter_conditions = FILTER_CONDITIONS

sectors = ['flood_agr', 'drought_agr', 'flood_urb', 'drought_shp']
input_file = 'data/stage3_portfolios_'
# button_path = 'Paper3_v1/data/logos/colorized'
button_path = 'https://raw.githubusercontent.com/JuliusSchlumberger/5_code/master/Paper3_v1/data/logos/colorized'
for sector in sectors:
    decision_tree(f'{input_file}{sector}.txt',sector, button_path, filter_conditions[sector])