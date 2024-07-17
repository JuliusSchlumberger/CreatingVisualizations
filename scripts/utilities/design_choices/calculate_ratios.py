from Paper3_v1.scripts.utilities.design_choices.apply_selections import apply_selections

# Function to calculate the ratios
def calculate_ratios(df, current_selections, risk_owner_hazard):
    ratios = []
    for pathway in df[risk_owner_hazard].unique():
        subset_df = df[df[risk_owner_hazard] == pathway]
        selected_data = apply_selections(subset_df, current_selections)
        ratio = len(selected_data) / len(subset_df)
        ratios.append(f'{int(ratio * 100)}%')
    return ratios
