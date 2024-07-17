def pathways_calculate_vertical_distance(dict_x, dict_y):
    # Reverse dict_x to group by x-values
    x_groups = {}
    for k, v in dict_x.items():
        if v not in x_groups:
            x_groups[v] = [k]
        else:
            x_groups[v].append(k)

    total_distance = 0

    # For each group of items that share the same x-value
    for x, keys in x_groups.items():
        # Extract measure numbers and corresponding y-values
        y_values = []
        for key in keys:
            measure = key.split('[')[0]  # Extract measure part
            if measure in dict_y:
                y_values.append(dict_y[measure])
            else:  # Handle 'current' or other special cases
                y_values.append(dict_y.get(measure, 0))

        # Calculate pairwise differences and add to total distance
        if len(y_values) > 1:
            for i in range(len(y_values) - 1):
                for j in range(i + 1, len(y_values)):
                    total_distance += abs(y_values[i] - y_values[j])

    return total_distance