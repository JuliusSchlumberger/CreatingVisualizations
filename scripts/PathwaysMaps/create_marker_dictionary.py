import matplotlib.pyplot as plt
import numpy as np

MEASURE_COLORS = {
            '0': '#bfbfbf',
            '1': '#ffcc99',
            '2': '#ffaa66',
            '3': '#ff8800',
            '4': '#cc6e00',
            '5': '#994c00',
            '6':'#cec3e6',
            '7': '#9d94cc',
            '8': '#4e429f',
            '9': '#2e2570',
            '10': '#b3cde3',
            '11': '#6497b1',
            '12': '#03396c',
            '13': '#011f4b',
            '14': '#011a30',
            '15': '#005b96',
            '16': '#b2dfdb',
            '17': '#00897b',
            '18': '#00695c',
            '19': '#004d40'
        }

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