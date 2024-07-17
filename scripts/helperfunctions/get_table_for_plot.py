def get_table_for_plot(df, risk_owner_hazard):
    pivot_df = df.pivot_table(
        index=risk_owner_hazard,
        columns='objective_parameter',
        values='normalized_values',
        aggfunc='sum'  # or 'mean', 'max', etc., depending on the required aggregation
    )
    reset_pivot = pivot_df.reset_index()
    reset_pivot.index = reset_pivot[risk_owner_hazard]
    # print(reset_pivot)
    pivot_text_df = df.pivot_table(
        index=risk_owner_hazard,
        columns='objective_parameter',
        values='Value',
        aggfunc='sum'  # or 'mean', 'max', etc., depending on the required aggregation
    )
    text_reset_pivot = pivot_text_df.reset_index()
    text_reset_pivot.index = text_reset_pivot[risk_owner_hazard]
    return reset_pivot, text_reset_pivot