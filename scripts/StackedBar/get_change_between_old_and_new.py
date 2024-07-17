import pandas as pd

def get_change_between_old_and_new(df_old, df_new, sector_objectives,risk_owner_hazard, normalized=True):
    tradeoffs = ['empty']
    other_objectives = ['empty']

    df_new.index.names = ['new_index_name' if x==risk_owner_hazard else x for x in df_new.index.names]

    df_old.index.names = ['new_index_name' if x==risk_owner_hazard else x for x in df_old.index.names]

    # Merge the two DataFrames on the specified columns
    merged_df = pd.merge(df_new, df_old,
                         on=[risk_owner_hazard],
                         suffixes=('', '_old'))

    for col in sector_objectives:
        diff_col = f'{col}_'  # New column name for the difference
        merged_df[diff_col] = merged_df[f'{col}'] - merged_df[f'{col}_old']  # if >0 normalized value for interaction is larger
        tradeoff = diff_col + 'tradeoff'
        synergy = diff_col + 'synergy'


        if normalized:
            merged_df[tradeoff] = merged_df[diff_col].copy().abs()
            merged_df[synergy] = merged_df[diff_col].copy().abs()

            merged_df.loc[merged_df[f'{col}'] < merged_df[f'{col}_old'], tradeoff] = 0
            merged_df.loc[merged_df[f'{col}'] > merged_df[f'{col}_old'], synergy] = 0
        else:
            merged_df[tradeoff] = merged_df[diff_col].copy().abs()
            merged_df[synergy] = merged_df[diff_col].copy().abs()

            merged_df.loc[merged_df[f'{col}'] < merged_df[f'{col}_old'], tradeoff] = 0
            merged_df.loc[merged_df[f'{col}'] > merged_df[f'{col}_old'], synergy] = 0

        tradeoffs += [tradeoff]
        other_objectives += [col, synergy]

    objectives_with_interactions = tradeoffs[1:] + other_objectives[1:]
    return merged_df, objectives_with_interactions
