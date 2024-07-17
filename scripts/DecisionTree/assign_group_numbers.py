

# Function to assign group numbers based on unique combinations
def assign_group_numbers(df, depth):
    """Assigns group numbers based on unique combinations of measures up to a specified depth."""
    combo_col_name = f'Group up to Measure {depth}'
    # Combine measures up to the specified depth to create a unique identifier for each combination
    df[combo_col_name] = df.iloc[:, :depth].apply(lambda row: '_'.join(row), axis=1)
    # Assign group numbers based on these unique combinations
    unique_combos = {combo: idx for idx, combo in enumerate(df[combo_col_name].unique(), 1)}
    df[combo_col_name] = df[combo_col_name].map(unique_combos)

    # Sort the DataFrame by the group columns in ascending order, prioritizing 'Group up to Measure 1'
    df = df.sort_values(
        by=[f'Group up to Measure {d}' for d in range(1,depth+1)])

    return df