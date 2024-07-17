import pandas as pd
import glob
import os
from Paper3_v1.scripts.utilities.generate_interaction_combinations import generate_combinations
from Paper3_v1.scripts.utilities.filter_options import SCENARIO_OPTIONS

def load_and_aggregate_files(input_path, rohs, output_path):
    # Dictionary to hold aggregated dataframes for each sector-hazard combination without interactions
    aggregated_data_no_interactions = {sh: [] for sh in rohs}
    interactions = generate_combinations(rohs,'')

    # Convert to list of lists with strings sorted
    list_of_lists = [sorted(item.split("&")) for item in interactions]

    # Convert to the final format with underscores
    keys = ["_".join(sublist) for sublist in list_of_lists]
    # Dictionary to hold data for combinations of 2, 3, and 4 sector-hazard combinations
    keys = keys[4:]
    aggregated_data_combinations = {sh: [] for sh in keys}

    # List all files matching the pattern
    files = glob.glob(os.path.join(input_path, 'pathway_combi_*_*_*_*.csv'))

    for file in files:
        # Extract strategies from filename
        strategies = [int(n) for n in os.path.basename(file)[:-4].split('_')[2:6]]

        # Load the dataframe
        df = pd.read_csv(file)

        # Check for no interaction dataframes and aggregate
        for i, strategy in enumerate(strategies):
            if strategy != 0 and all(s == 0 for j, s in enumerate(strategies) if j != i):
                aggregated_data_no_interactions[rohs[i]].append(df)

        # For combinations, create a unique key for the combination and aggregate
        active_strategies = [rohs[i] for i, strategy in enumerate(strategies) if strategy != 0]
        if len(active_strategies) > 1:
            key = '_'.join(sorted(active_strategies))
            aggregated_data_combinations[key].append(df)

    # Save the aggregated dataframes
    for sh, df_list in aggregated_data_no_interactions.items():
        if len(df_list) > 1:
            df = pd.concat(df_list, ignore_index=True)
        else:
            df = df_list[0]
        df[rohs] = df.pw_combi.str.split('_', expand=True)

        # add all scenario of interest combinations
        result_dfs = []
        for scenario in SCENARIO_OPTIONS:

            scenario_str = '&'.join(scenario)
            filtered_df = df[df['cc_scenario'].isin(scenario)]

            filtered_df['scenario_of_interest'] = scenario_str
            filtered_df = filtered_df.drop(columns=['cc_scenario'])
            result_dfs.append(filtered_df)

        final_df = pd.concat(result_dfs, ignore_index=True)

        final_df.to_csv(f'{output_path}/objectives_for_count_no_interactions_{sh}.csv', index=False)

    for combo, df_list in aggregated_data_combinations.items():
        if len(df_list) > 1:
            df = pd.concat(df_list, ignore_index=True)
        else:
            df = df_list[0]
        # df = pd.concat(df_list, ignore_index=True)
        df[rohs] = df.pw_combi.str.split('_', expand=True)

        # add all scenario of interest combinations
        result_dfs = []
        for scenario in SCENARIO_OPTIONS:
            scenario_str = '&'.join(scenario)
            filtered_df = df[df['cc_scenario'].isin(scenario)]

            filtered_df['scenario_of_interest'] = scenario_str
            filtered_df = filtered_df.drop(columns=['cc_scenario'])
            result_dfs.append(filtered_df)

        final_df = pd.concat(result_dfs, ignore_index=True)

        final_df.to_csv(f'{output_path}/objectives_for_count_combinations_{combo}.csv', index=False)
