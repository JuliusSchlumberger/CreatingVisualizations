

def apply_selections(subset_df, current_selections):
    selected_data = subset_df.copy()
    for axis, ranges in current_selections.items():
        for range_sel in ranges:
            if axis in subset_df.columns:  # Check if axis is still valid
                selected_data = selected_data[selected_data[axis].between(range_sel[0], range_sel[1])]
    return selected_data
