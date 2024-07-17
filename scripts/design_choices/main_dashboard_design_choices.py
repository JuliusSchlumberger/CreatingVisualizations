from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


FIGSIZES = {
    'options_figure': (12,5.5)
}


# Define a custom discrete colorscale
# COLORSCALE_HEATMAP = [
#     [0.0, '#fa8de0'], [0.2, '#fa8de0'],  # First segment
#     [0.2, '#f2a7c2'], [0.4, '#f2a7c2'],  # Second segment
#     [0.4, '#f3f3f3'], [0.6, '#f3f3f3'],  # Third segment
#     [0.6, '#d7d57f'], [0.8, '#d7d57f'],  # Fourth segment
#     [0.8, '#c3ea57'], [1.0, '#c3ea57']  # Fifth and last segment
# ]
COLORSCALE_HEATMAP = px.colors.sequential.Greens_r

COLORSCALE = [
    '#fa8de0',  # 0.0 to 0.2
    '#f2a7c2',  # 0.2 to 0.4
    '#f3f3f3',  # 0.4 to 0.6
    '#d7d57f',  # 0.6 to 0.8
    '#c3ea57'   # 0.8 to 1.0
]


# COLORSCALE_PCP = [[0, 'grey'],[.5, 'red'],  [1, 'red']]
COLORSCALE_PCP = [[1000, 'Grey' ]]
COLORSCALE_NAMES = {1000: 'without interactions',}
# COLORSCALE_PCP = [['with interaction', '#c3ea57' ],['without interaction', 'blue'],[.6, 'blue'],['baseline', '#f3f3f3'], [1, '#fa8de0']]
# COLORSCALE_PCP = ['fa8de0', 'f3f3f3', 'f3f3f3', 'c3ea57']

MEASURE_COLORS = {
    list(ROH_DICT_INV.keys())[0]: ['#b3cde3', '#6497b1', '#005b96', '#03396c', '#011f4b', '#011a30'],
    list(ROH_DICT_INV.keys())[1]: ['#ffcc99', '#ffaa66', '#ff8800', '#cc6e00', '#994c00', '#663300'],
    list(ROH_DICT_INV.keys())[2]: ['#b2dfdb', '#80cbc4', '#4db6ac', '#00897b', '#00695c', '#004d40'],
    list(ROH_DICT_INV.keys())[3]: ['#cec3e6', '#9d94cc', '#6e63b3', '#4e429f', '#3b318c', '#2e2570']
}

OBJECTIVE_COLORS = {
    list(ROH_DICT_INV.keys())[0]: ['#b3cde3', '#6497b1', '#005b96', '#03396c', '#011f4b', '#011a30'],
    list(ROH_DICT_INV.keys())[1]: ['#ffcc99', '#ff8800'],
    list(ROH_DICT_INV.keys())[2]: ['#b2dfdb', '#4db6ac'],
    list(ROH_DICT_INV.keys())[3]: ['#cec3e6', '#6e63b3']
}
MEASURE_NUMBERS = {
            'no_measure': 100,
            'd_resilient_crops': 1,
            'd_rain_irrigation': 2,
            'd_gw_irrigation': 3,
            'd_riv_irrigation': 4,
            'd_soilm_practice': 5,
            'd_multimodal_transport': 6,
            'd_medium_ships': 7,
            'd_small_ships': 8,
            'd_dredging': 9,
            'f_resilient_crops': 10,
            'f_ditches': 11,
            'f_local_support': 12,
            'f_dike_elevation_s': 13,
            'f_dike_elevation_l': 14,
            'f_maintenance': 15,
            'f_room_for_river': 16,
            'f_wet_proofing_houses': 17,
            'f_local_protect': 18,
            'f_awareness_campaign': 19
        }
MEASURE_COLORS = {
            '100': '#f3f3f3',
            '0': '#f3f3f3',
            '1': '#ffaa66',
            '2': '#ff8800',
            '3': '#cc6e00',
            '4': '#994c00',
            '5': '#663300',
            '6':'#cec3e6',
            '7': '#9d94cc',
            '8': '#4e429f',
            '9': '#2e2570',
            '10': '#b3cde3',
            '11': '#6497b1',
            '12': '#03396c',
            '13': '#011f4b',
            '14': '#011a30',
            '15': '#005b96',
            '16': '#b2dfdb',
            '17': '#00897b',
            '18': '#00695c',
            '19': '#004d40'
        }

# Generate 19 colors from the viridis colormap
viridis = plt.get_cmap('plasma_r')
new_colors = [mcolors.to_hex(viridis(i / 19)) for i in range(1, 20)]

# Replace the colors for keys 1 to 19
for i in range(1, 20):
    MEASURE_COLORS[str(i)] = new_colors[i-1]


# Generate colors
yellow_colors = plt.get_cmap('Oranges')(np.linspace(0.3, 0.8, 5))  # Shades of yellow
green_colors = plt.get_cmap('Purples')(np.linspace(0.4, 0.8, 4))  # Shades of green
bluegreen_colors = plt.get_cmap('viridis')(np.linspace(0.1, .9, 10))  # Shades of blue-green

# Update MEASURE_COLORS dictionary
for i in range(1, 6):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(yellow_colors[i-1])

for i in range(6, 10):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(green_colors[i-6])

for i in range(10, 20):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(bluegreen_colors[i-10])

# Pathways Maps
MAX_X_OFFSET = .7 # will do adjustments in horizontal direction. Needs adjustment if lines of different measures start overlap.
MAX_Y_OFFSET = .48 # will do adjustments in vertical direction between instances. Needs adjustment if markers overlap.
