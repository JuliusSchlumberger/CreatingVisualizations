import os
import fnmatch
from scripts.main_central_path_directions import DIRECTORY_PATHWAYS_GENERATOR
from scripts.filter_options import ROBUSTNESS_METRICS_LIST, SCENARIO_OPTIONS
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV, TIMEHORIZONS_INV
from scripts.PathwaysMaps.create_pathways_maps import create_pathways_maps

def find_files_with_string(directory, search_string):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, f'*{search_string}*'):
            matching_files.append(os.path.join(root, filename))
    return matching_files

foci = ['drought_agr_Wp_50%', 'flood_agr_Wp_50%']
for risk_owner_hazard in ROH_DICT_INV:
    for scenarios in SCENARIO_OPTIONS:
        focus = f'{risk_owner_hazard}_{SCENARIO_OPTIONS}_50%'
        focus = foci[1]

        savepath = f'figures/PathwaysMaps/{risk_owner_hazard}/pathways_map_{risk_owner_hazard}'

        # Initialize Pathways Generator
        line_choice = 'pathways_and_unique_lines'  # options: 'pathways', 'overlay', 'pathways_and_unique_lines'
        input_with_pathways = True  # True if input file contains pathway numbers
        optimize_positions = False  # Automatically adjust positions to minimize vertical distance
        num_iterations = 'all'  # Number of iterations for optimization, if False, all combinations run
        ylabels = 'logos'  # options: 'logos', 'names', 'numbers'

        # create base figure as png and as plotly
        file_offset = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/{focus}_optimized_offset'
        file_base = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/{focus}_optimized_base'

        create_pathways_maps(focus, line_choice, input_with_pathways,optimize_positions, file_offset, file_base, num_iterations, ylabels, savepath, interaction_identifier=False)

        matching_files = find_files_with_string(DIRECTORY_PATHWAYS_GENERATOR, f'all_sequences_{focus}')

        # loop trhough all files in directory and check if the file starts with same name as the no_interaction_file
        for file in matching_files:
            if '&' in file: # Interaction
                identifier = file.split(focus)[1].split('.')[0]

                savepath = f'figures/PathwaysMaps/{risk_owner_hazard}/pathways_map_{risk_owner_hazard}_combi{identifier}'

                # Initialize Pathways Generator
                line_choice = 'pathways_and_unique_lines'  # options: 'pathways', 'overlay', 'pathways_and_unique_lines'
                input_with_pathways = True  # True if input file contains pathway numbers
                optimize_positions = False  # Automatically adjust positions to minimize vertical distance
                num_iterations = 'all'  # Number of iterations for optimization, if False, all combinations run
                ylabels = 'logos'  # options: 'logos', 'names', 'numbers'

                create_pathways_maps(focus, line_choice, input_with_pathways, optimize_positions, file_offset,
                                     file_base, num_iterations, ylabels, savepath, interaction_identifier=identifier)
