import matplotlib.pyplot as plt
import numpy as np
from scripts.design_choices.main_dashboard_design_choices import MEASURE_COLORS

def create_marker_dictionary(actions, base_y_values, instance_dict, y_offsets):
    action_pairs = {}
    # Parse the keys to organize data
    data = {}
    for key, value in actions.items():
        parts = key.split('[')
        measure = parts[0].split('(')[1][1:]
        instance = parts[1].split(']')[0]
        base_y = base_y_values.get(measure, 0)  # Default to 0 if measure not in base_y_values

        marker = 'o'
        action_type = "Begin" if "Begin" in key else "End"
        color = MEASURE_COLORS[measure]  # Assign color based on measure
        facecolor = 'w' if "End" in key else color  # Hollow for "End", filled for "Begin"

        # Adjust y-values slightly based on instance (unique measure-instance combination)
        instance_number = instance_dict[measure][instance]
        y_adjustment = y_offsets[str(instance_number)]
        value_adjusted = np.array([value[0], int(base_y) + y_adjustment])

        # Store in data dictionary
        if measure not in data:
            data[measure] = []
        data[measure].append((value_adjusted, marker, color, facecolor))

        # Prepare coordinates for line drawing
        coord_key = (measure, instance)
        if coord_key not in action_pairs:
            action_pairs[coord_key] = {}
        action_pairs[coord_key][action_type] = value_adjusted
    return action_pairs, data