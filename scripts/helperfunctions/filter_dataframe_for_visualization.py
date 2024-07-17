from scripts.main_central_path_directions import ROH_LIST
from scripts.map_system_parameters import SECTOR_OBJECTIVES


def filter_dataframe_for_visualization(df, risk_owner_hazard, timehorizon, scenarios, performance_metric):

    # Filter the dataframe based on selections
    selected_scenarios = '&'.join(scenarios)

    filtered_df = df[
        (df['year'].isin([timehorizon])) &  # Assuming timehorizon is a single selection, not a list
        (df['scenario_of_interest'] == selected_scenarios) &
        (df['performance_metric'].isin(performance_metric)) &
        (df.objective_parameter.isin(SECTOR_OBJECTIVES[risk_owner_hazard]))
        ].copy()
    filtered_df[ROH_LIST] = filtered_df.pw_combi.str.split('_', expand=True)

    # Split 'pw_combi' column and expand into separate columns
    filtered_df.loc[:,ROH_LIST] = filtered_df[ROH_LIST].astype(int)

    # Identify columns in B not in A
    columns_to_drop = [column for column in ROH_LIST if column != risk_owner_hazard]

    # Drop these columns from the DataFrame
    filtered_df = filtered_df.drop(columns=columns_to_drop, errors='ignore')

    return filtered_df
