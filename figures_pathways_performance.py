import pandas as pd
import re
import os
import plotly.graph_objects as go  # Import Plotly's graph_objects module
from scripts.design_choices.main_dashboard_dropdowns import PATHWAYS_TO_HIGHLIGHT, ROH_DICT,ROH_DICT_INV, SECTOR_OBJECTIVES_BUTTONS, TIMEHORIZONS_INV

from scripts.main_central_path_directions import ROH_LIST
from scripts.map_system_parameters import SECTOR_OBJECTIVES
from scripts.ParallelCoordinates.Parallel_Coordinates_Plot import Parallel_Coordinates_Plot
from scripts.StackedBar.Stacked_Bar_Plot import Stacked_Bar_Plot
from scripts.Heatmap.Heatmap import Heatmap
from scripts.filter_options import ROBUSTNESS_METRICS_LIST, SCENARIO_OPTIONS
from scripts.helperfunctions.filter_dataframe_for_visualization import filter_dataframe_for_visualization
from scripts.design_choices.main_dashboard_dropdowns import SCENARIOS_INV
from scripts.main_central_path_directions import DIRECTORY_INTERACTIONS

import pathlib

performance_df_dict = {
    ROH_LIST[0]: f'{DIRECTORY_INTERACTIONS}/performance_{ROH_LIST[0]}_no_interactions.csv',
    ROH_LIST[1]: f'{DIRECTORY_INTERACTIONS}/performance_{ROH_LIST[1]}_no_interactions.csv',
    ROH_LIST[2]: f'{DIRECTORY_INTERACTIONS}/performance_{ROH_LIST[2]}_no_interactions.csv',
    ROH_LIST[3]: f'{DIRECTORY_INTERACTIONS}/performance_{ROH_LIST[3]}_no_interactions.csv'}

# Function to extract the identifier from the filename
def extract_identifier(filename):
    match = re.search(r'combi_(.*?)\.', filename)
    if match:
        return match.group(1)
    return None

def pathways_performance(scenarios, plot_type, risk_owner_hazard, performance_metric, timehorizon):
    if len(scenarios) == 1:
        scenarios_title = f'{SCENARIOS_INV[scenarios[0]]} climate scenario'
    else:
        better_names = [SCENARIOS_INV[scen] for scen in scenarios]
        scenarios_title = 'across multiple climate scenarios [' + ' & '.join(better_names) + ']'

    figure_title = f'Analyse Pathways Performance ({timehorizon} years; {scenarios_title})'

    #  Load Data for normal figure
    performance_path_of_interest = performance_df_dict[risk_owner_hazard]
    performance_df_of_interest = pd.read_csv(f'{performance_path_of_interest}')

    # Identify files for interaction plots
    identifier_for_interactions = performance_path_of_interest[:-19]    # split off no_interactions.csv


    if plot_type == 'PCP':
        if performance_metric in ROBUSTNESS_METRICS_LIST[:-1]:
            # relevant_metrics = ROBUSTNESS_METRICS_LIST[:-1]
            relevant_metrics = [performance_metric]
        else:
            relevant_metrics = [performance_metric]
    else:
        relevant_metrics = [performance_metric]
    filtered_df = filter_dataframe_for_visualization(performance_df_of_interest, risk_owner_hazard,
                                                     timehorizon,
                                                     scenarios,
                                                     relevant_metrics)

    if plot_type == 'PCP':
        fig = Parallel_Coordinates_Plot(df=filtered_df, risk_owner_hazard=risk_owner_hazard, figure_title=figure_title, performance_metric=performance_metric)

        # Loop through the files in the directory
        for filename in os.listdir(DIRECTORY_INTERACTIONS):
            # Check if the filename starts with the specified string
            if filename.startswith(f'{identifier_for_interactions}combi_'):
                # Perform your desired operation on the file
                interaction_filepath = os.path.join(DIRECTORY_INTERACTIONS, filename)
                interaction_df = pd.read_csv(interaction_filepath)
                interaction_filtered_df = filter_dataframe_for_visualization(performance_df_of_interest, risk_owner_hazard,
                                                                 timehorizon,
                                                                 scenarios,
                                                                 relevant_metrics)

                fig = Parallel_Coordinates_Plot(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                                                figure_title=figure_title, performance_metric=performance_metric, df_interaction=interaction_filtered_df)

    elif plot_type == 'StackedBar':
        fig = Stacked_Bar_Plot(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                                sector_objectives=SECTOR_OBJECTIVES[risk_owner_hazard], figure_title=figure_title)
    elif plot_type == 'Heatmap':
        fig = Heatmap(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                       sector_objectives=SECTOR_OBJECTIVES[risk_owner_hazard], figure_title=figure_title)
    else:
        fig = go.Figure()

    pathlib.Path(f'figures/{plot_type}/{risk_owner_hazard}/').mkdir(parents=True, exist_ok=True)
    fig.write_json(f'figures/{plot_type}/{risk_owner_hazard}/plot_{timehorizon}_{scenario_str}_{performance_metric}.json')
    # fig.write_html(
    #     f'Dashboard_v1/assets/figures/{plot_type}/{risk_owner_hazard}/plot_{timehorizon}_{scenario_str}_{performance_metric}.html')


def pathways_performance_with_interactions(scenarios, plot_type, risk_owner_hazard, performance_metric, timehorizon):
    if len(scenarios) == 1:
        scenarios_title = f'{SCENARIOS_INV[scenarios[0]]} climate scenario'
    else:
        better_names = [SCENARIOS_INV[scen] for scen in scenarios]
        scenarios_title = 'across multiple climate scenarios [' + ' & '.join(better_names) + ']'

    figure_title = f'Analyse Pathways Performance ({timehorizon} years; {scenarios_title})'

    #  Load Data for normal figure
    performance_path_of_interest = performance_df_dict[risk_owner_hazard]
    performance_df_of_interest = pd.read_csv(f'{performance_path_of_interest}')

    # Identify files for interaction plots
    identifier_for_interactions = performance_path_of_interest[:-20].split('/')[-1]  # split off no_interactions.csv
    print(identifier_for_interactions)

    if plot_type == 'PCP':
        if performance_metric in ROBUSTNESS_METRICS_LIST[:-1]:
            # relevant_metrics = ROBUSTNESS_METRICS_LIST[:-1]
            relevant_metrics = [performance_metric]
        else:
            relevant_metrics = [performance_metric]
    else:
        relevant_metrics = [performance_metric]
    filtered_df = filter_dataframe_for_visualization(performance_df_of_interest, risk_owner_hazard,
                                                     timehorizon,
                                                     scenarios,
                                                     relevant_metrics)

    for filename in os.listdir(DIRECTORY_INTERACTIONS):
        # Check if the filename starts with the specified string
        # print(filename)
        if f'{identifier_for_interactions}_combi_' in filename:
            print(filename)
            # Perform your desired operation on the file
            interaction_filepath = os.path.join(DIRECTORY_INTERACTIONS, filename)
            identifier = extract_identifier(filename)
            interaction_df = pd.read_csv(interaction_filepath)
            interaction_filtered_df = filter_dataframe_for_visualization(interaction_df,
                                                                         risk_owner_hazard,
                                                                         timehorizon,
                                                                         scenarios,
                                                                         relevant_metrics)
            if plot_type == 'PCP':
                fig = Parallel_Coordinates_Plot(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                                                figure_title=figure_title, performance_metric=performance_metric,
                                                df_interaction=interaction_filtered_df)

            elif plot_type == 'StackedBar':
                fig = Stacked_Bar_Plot(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                                        sector_objectives=SECTOR_OBJECTIVES[risk_owner_hazard], figure_title=figure_title, df_interaction=interaction_filtered_df)
            elif plot_type == 'Heatmap':
                fig = Heatmap(df=filtered_df, risk_owner_hazard=risk_owner_hazard,
                               sector_objectives=SECTOR_OBJECTIVES[risk_owner_hazard], figure_title=figure_title, df_interaction=interaction_filtered_df)
            else:
                fig = go.Figure()

            pathlib.Path(f'figures/{plot_type}/{risk_owner_hazard}/').mkdir(parents=True, exist_ok=True)
            fig.write_json(f'figures/{plot_type}/{risk_owner_hazard}/plot_{timehorizon}_{scenario_str}_{performance_metric}_combi_{identifier}.json')
            # fig.write_html(
            #     f'figures/{plot_type}/{risk_owner_hazard}/plot_{timehorizon}_{scenario_str}_{performance_metric}_combi_{identifier}.html')


# for plot_type in ['StackedBar', 'PCP', 'Heatmap']:
# No Interactions
for plot_type in ['Heatmap']:
    for risk_owner_hazard in ROH_DICT_INV:
        for performance_metric in ROBUSTNESS_METRICS_LIST:
            for timehorizon in TIMEHORIZONS_INV:
            # for timehorizon in {100: 'next 100 years'}:
                for scenarios in SCENARIO_OPTIONS:
                    if len(scenarios) > 1:
                        scenario_str = '&'.join(scenarios)
                    else:
                        scenario_str = scenarios[0]
                    pathways_performance(scenarios, plot_type, risk_owner_hazard, performance_metric, timehorizon)
                    pathways_performance_with_interactions(scenarios, plot_type, risk_owner_hazard, performance_metric,
                                                           timehorizon)




