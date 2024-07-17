# Function to calculate position measures based on the logic described
def calculate_position_measure(df, current_measure, reference_measure):
    # Calculate the unique counts for the reference measure to determine uniqueness
    unique_counts = df.groupby(reference_measure)[reference_measure].transform('count')
    # If unique (count == 1), keep the current position measure value
    # Otherwise, calculate the average of the current position measure for rows with the same reference measure value
    df[f'Position_measure_{current_measure}'] = df.groupby(reference_measure)[f'Position_measure_{current_measure+1}'].transform(lambda x: (x.min() + x.max()) / 2) \
        .where(unique_counts > 1, df[f'Position_measure_{current_measure+1}'])
    return df