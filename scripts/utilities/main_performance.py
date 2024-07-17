from Paper3_v1.scripts.process_inputs.get_normalized_performance import get_normalized_performance
from Paper3_v1.scripts.process_inputs.add_cost import add_costs
from Paper3_v1.scripts.utilities.map_system_parameters import SYSTEM_PARAMETERS_LIST
from Paper3_v1.scripts.utilities.create_directory import create_directory_if_not_exists
from Paper3_v1.scripts.process_inputs.create_benchmark_for_normalization import create_benchmark_for_normalization
from Paper3_v1.scripts.process_inputs.get_objective_values import get_objective_values
from Paper3_v1.scripts.process_inputs.get_timehorizons_of_interest import get_timehorizons
from Paper3_v1.scripts.process_inputs.get_performance_values import get_performance_values
from Paper3_v1.scripts.utilities.get_pathway_combi import get_pathway_combi
from Paper3_v1.scripts.utilities.get_pathway_interaction_files import load_and_aggregate_files
from Paper3_v1.scripts.process_inputs.get_performance_across_interactions import get_performance_across_interactions


import pandas as pd
import os

def create_benchmark_case(benchmark_file_path_in, benchmark_file_path_out):
    df_with_cost = add_costs(benchmark_file_path_in)

    system_performance_df = df_with_cost[df_with_cost['system_parameter'].isin(SYSTEM_PARAMETERS_LIST)]

    create_benchmark_for_normalization(system_performance_df, benchmark_file_path_out)


def create_performance_sets(set_of_model_outputs_files, system_parameter_directory):

    create_directory_if_not_exists(system_parameter_directory)

    # Do for each file in set
    for model_output in set_of_model_outputs_files:
        df_with_cost = add_costs(model_output)
        system_performance_df = df_with_cost[df_with_cost['system_parameter'].isin(SYSTEM_PARAMETERS_LIST)]

        pathway_combo = get_pathway_combi(model_output)

        system_performance_df.to_csv(f'{system_parameter_directory}/pathways_combi_{pathway_combo}.csv', index=False)


def get_objective_performance_for_timehorizons(set_of_model_outputs_files,system_parameter_directory,benchmark_file_path,performance_directory_path):

    create_directory_if_not_exists(performance_directory_path)

    for model_output in set_of_model_outputs_files:
        pathway_combo = get_pathway_combi(model_output)

        objective_df = get_objective_values(f'{system_parameter_directory}/pathways_combi_{pathway_combo}.csv')

        timehorizon_df = get_timehorizons(objective_df)

        performance_df = get_performance_values(timehorizon_df)

        get_normalized_performance(performance_df, benchmark_file_path,
                                   f'{performance_directory_path}/pathway_combi_{pathway_combo}_normalized.csv')

def combine_all_performance_sets(directory_path, rohs, outputfile_path):
    create_directory_if_not_exists(outputfile_path)

    load_and_aggregate_files(directory_path, rohs, outputfile_path)

def get_pathways_performances_across_interactions(directory_path, roh, outputfile_path):
    create_directory_if_not_exists(outputfile_path)

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        df = pd.read_csv(file_path)
        df = get_performance_across_interactions(df, roh)

        df.to_csv(f'{outputfile_path}/{filename}')
