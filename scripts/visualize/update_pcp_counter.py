import re
import pandas as pd
from Paper3_v1.scripts.utilities.map_system_parameters import SECTOR_OBJECTIVES, AXIS_LABELS
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import COLORSCALE
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_dropdowns import ROH_DICT_INV



def update_pcp_counter(df, restyle_data, dimensions, current_selections, scenarios, interactions_of_interest, risk_owner_hazard, timehorizon, existing_figure, column):
    changes = restyle_data[0]
    for change_key in changes.keys():
        # Check if this change is for a dimension's constraintrange
        match = re.match(r'dimensions\[(\d+)\].constraintrange', change_key)
        if match:
            axis_index = int(match.group(1))
            # Ensure axis index is within bounds
            if axis_index < len(dimensions):
                axis_name = dimensions[axis_index]['label']
                ranges = changes[change_key]
                if ranges is None:
                    # If the selection is cleared, remove the axis from current_selections
                    current_selections.pop(axis_name, None)
                else:
                    # Update current_selections with the new range for this axis
                    current_selections[axis_name] = ranges

    # Filter data to populate table
    # print(current_selections)
    scenario_str = '&'.join(scenarios)

    count_df = df[
        (df[
             'year'] == timehorizon) &  # Assuming timehorizon is a single selection, not a list
        (df['scenario_of_interest'] == scenario_str) &
        (df.objective_parameter.isin(
            SECTOR_OBJECTIVES[risk_owner_hazard]))
        ].copy()

    # Convert longtable into pivot-table
    relevant_pivot_table = pd.pivot_table(count_df, values='Value',
                                          columns=['objective_parameter'],
                                          index=[risk_owner_hazard, 'climvar',
                                                 'scenario_of_interest']).reset_index()

    relevant_pivot_table = relevant_pivot_table.rename(columns=AXIS_LABELS)
    relevant_pivot_table = relevant_pivot_table.rename(columns=ROH_DICT_INV)

    # Create subset based on selected ranges
    filtered_range = relevant_pivot_table.copy()
    for axis, ranges in current_selections.items():
        for range_sel in ranges:
            subset = filtered_range.copy()
            subset = subset[subset[axis].between(range_sel[0], range_sel[1])]
            filtered_range = subset.copy()

    counts_not_filtered = relevant_pivot_table.groupby(ROH_DICT_INV[risk_owner_hazard]).size().reset_index(name='not_filtered')

    counts_not_filtered['not_filtered'].replace({0: 1}, inplace=True)
    counts_filtered = filtered_range.groupby(ROH_DICT_INV[risk_owner_hazard]).size().reset_index(
        name='filtered')

    # Ensure that no NaN values are in table
    counts_filtered = counts_filtered.fillna(0)

    # Merge the counts on risk_owner_hazard
    merged_counts = pd.merge(counts_not_filtered, counts_filtered, on=ROH_DICT_INV[risk_owner_hazard], how='outer')

    # Calculate the ratio of counts
    merged_counts['ratio'] = merged_counts['filtered'] / merged_counts['not_filtered'] * 100
    merged_counts = merged_counts.fillna(0)
    table_data = merged_counts['ratio'].apply(lambda x: f'{x:.0f}%').tolist()
    # print(table_data_dict[key])

    # Modify the table subplot within updated_figure with new_counts
    existing_figure['data'][1]['cells']['values'][column] = table_data
    existing_figure['data'][1]['cells']['values'][0] = merged_counts[ROH_DICT_INV[risk_owner_hazard]]

    # Normalize function (assuming values are in 0 to 100 range)
    def normalize_to_color(value, scale):
        # Convert percentage to a 0-1 scale
        normalized_value = value / 100
        # Determine the index in the colorscale
        index = min(int(normalized_value / 0.2), len(scale) - 1)
        return scale[index]

    # Apply the color mapping to a column (e.g., 'no_interaction')
    new_colors = merged_counts['ratio'].apply(lambda x: normalize_to_color(x, COLORSCALE)).tolist()
    print(existing_figure)

    if 'fill' not in existing_figure['data'][1]['cells']:
        existing_figure['data'][1]['cells']['fill']['color'] = [['white'] * len(table_data) for _ in
                                                             existing_figure['data'][1]['cells']['values']]

    # Now, update the fill_color for the specified column
    existing_figure['data'][1]['cells']['fill']['color'][column] = new_colors

    return existing_figure