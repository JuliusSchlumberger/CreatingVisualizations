import json
import numpy as np
from scripts.PathwaysMaps._optimize_positions import create_optimized_positions
from scripts.PathwaysMaps._create_marker_dictionary import create_marker_dictionary
from scripts.PathwaysMaps._instance_dictionary import create_instance_dictionary
from scripts.PathwaysMaps._base_figure import base_figure, other_figure
from scripts.PathwaysMaps._base_figure_plotly import base_figure_plotly, pathways_change_plotly
from scripts.PathwaysMaps._get_network_dicts import get_network_dicts
import matplotlib.pyplot as plt


class Pathways_Generator_Advanced():
    """
    Generates visual representations of pathways with optional optimization and logos.

    Parameters:
    - input_file: Path to the input file containing sequences and pathways information.
    - file_sequence_only: Path to save the extracted sequences only.
    - file_tipping_points: Path to the file containing tipping points.
    - file_offset: Path to save the optimal offset JSON file.
    - file_base: Path to save the optimal base y-values JSON file.
    - savepath: Path to save the resulting figure.
    - renaming_dict: Dictionary for renaming measures.
    - replacing_measure: Dictionary mapping measures to their replacements.
    - measure_numbers_inv: Dictionary mapping measure numbers to their inverse mappings.
    - max_x_offset: Maximum x-offset value.
    - max_y_offset: Maximum y-offset value.
    - measure_colors: Dictionary mapping measure identifiers to color strings.
    - with_pathways: Boolean indicating whether to include pathways information.
    - unique_lines: Boolean indicating whether each new x-position should get a unique instance number.
    - optimize: Boolean indicating whether to optimize the positions.
    - num_iterations: Optional; the number of iterations to run for optimization. If False, all permutations are considered.
    - ylabels: String whether to add logos, names or numbers to the plot.

    Returns:
    - None
    """

    def __init__(self, measure_colors, measure_numbers_inv, replacing_measure, line_choice, input_with_pathways):
        """
        Initializes the Pathways_Generator_Advanced instance.

        Parameters:
        - measure_colors: Dictionary mapping measure identifiers to color strings.
        - measure_numbers_inv: Dictionary mapping measure numbers to their inverse mappings.
        - replacing_measure: Dictionary mapping measures to their replacements.
        - line_choice: Design choice for line representation.
        - input_with_pathways: Boolean indicating whether the input file contains pathway numbers.
        """
        self.line_choice = line_choice
        self.input_with_pathways = input_with_pathways
        self.measure_colors = measure_colors
        self.measure_numbers_inv = measure_numbers_inv
        self.replacing_measure = replacing_measure

    def create_start_files(self, input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict,
                           max_x_offset, initial_measures_in_pathways=False, initial_base_y_values=False,
                           instance_dict=False, initial_max_instance=False, x_position_dict=False):
        """
        Creates initial files and dictionaries needed for generating pathways.

        Parameters:
        - input_file_with_pathways: Path to the input file containing pathways information.
        - file_sequence_only: Path to save the extracted sequences only.
        - file_tipping_points: Path to the file containing tipping points.
        - renaming_dict: Dictionary for renaming measures.
        - max_x_offset: Maximum x-offset value.
        - initial_measures_in_pathways: Initial measures in pathways (optional).
        - initial_base_y_values: Initial base y-values (optional).
        - instance_dict: Initial instance dictionary (optional).
        - initial_max_instance: Initial maximum instance number (optional).
        - x_position_dict: Initial x-position dictionary (optional).

        Returns:
        - instance_dict: Updated instance dictionary.
        - actions: Dictionary of actions.
        - action_transitions: List of action transitions.
        - base_y_values: Updated base y-values dictionary.
        - x_offsets: Dictionary of x-offsets.
        - measures_in_pathways: Updated measures in pathways dictionary.
        - max_instance: Maximum instance number.
        - x_position_dict: Updated x-position dictionary.
        """
        # Create files from pathways generator input files
        actions, action_transitions, base_y_values, x_offsets, measures_in_pathways = get_network_dicts(self,
                                                                                                        input_file_with_pathways,
                                                                                                        file_sequence_only,
                                                                                                        file_tipping_points,
                                                                                                        renaming_dict,
                                                                                                        max_x_offset)

        if initial_measures_in_pathways:
            # Update set of measures in pathways
            for pathway in measures_in_pathways.keys():
                initial_measures = initial_measures_in_pathways[pathway]
                new_measures = measures_in_pathways[pathway]
                measures_in_pathways[pathway] = np.concatenate(
                    [initial_measures, [m for m in new_measures if m not in initial_measures]], axis=0)

        if initial_base_y_values:
            # Avoid that specific numbers are overriding each other because of different order in input files
            initial_keys = list(initial_base_y_values.keys())
            new_keys = list(base_y_values.keys())
            all_keys = set(initial_keys + new_keys)
            num_y_positions = len(all_keys)

            pos_y_positions = np.linspace(0, int(np.floor(num_y_positions / 2)), int(np.floor(num_y_positions / 2)) + 1)
            neg_y_positions = np.linspace(-int(np.ceil(num_y_positions / 2)), 0, int(np.ceil(num_y_positions / 2)) + 1)[
                              ::-1]
            all_y_positions = np.concatenate([pos_y_positions, neg_y_positions[1:]], axis=0)
            base_y_values = {}
            for tick, y_key in enumerate(all_keys):
                base_y_values[y_key] = all_y_positions[tick]

        # Get number of instances with different tipping points per measure, decide if lines with same tipping point are overlaid or not
        if not instance_dict:
            instance_dict = {}  # Dictionary to store instance numbers for each measure
        if not initial_max_instance:
            initial_max_instance = 0  # Track the highest instance number assigned
        if not x_position_dict:
            x_position_dict = {}  # Dictionary to track end positions for measures
        instance_dict, max_instance, x_position_dict = create_instance_dictionary(self, actions, instance_dict,
                                                                                  initial_max_instance, x_position_dict)

        return instance_dict, actions, action_transitions, base_y_values, x_offsets, measures_in_pathways, max_instance, x_position_dict

    def optimize_positions(self, instance_dict, actions, action_transitions, base_y_values, max_instance, max_y_offset,
                           file_offset, file_base, num_iterations, optimize_positions='both'):
        """
        Optimizes the positions to minimize total vertical distance for action transitions.

        Parameters:
        - instance_dict: Dictionary mapping measures to their instances.
        - actions: Dictionary of actions.
        - action_transitions: List of action transitions.
        - base_y_values: Dictionary of base y-values.
        - max_instance: Maximum instance number.
        - max_y_offset: Maximum y-offset value.
        - file_offset: Path to save the optimal offset JSON file.
        - file_base: Path to save the optimal base y-values JSON file.
        - num_iterations: Optional; the number of iterations to run for optimization. If 'all', all permutations are considered.
        - optimize_positions: Specifies whether to optimize 'both', 'offset', or 'base_y' positions.

        Returns:
        - None
        """
        # Calculate y-offsets for instances
        y_offsets1 = np.linspace(0, max_y_offset, int(np.floor(max_instance / 2)) + 1)
        y_offsets2 = np.linspace(-max_y_offset, 0, int(np.ceil(max_instance / 2)) + 1)[::-1]

        # Initialize the rearranged list
        rearranged_offsets = []

        # Interleave the values from y_offsets1 and y_offsets2
        for i in range(1, len(y_offsets1)):
            rearranged_offsets.append(y_offsets1[i])
            rearranged_offsets.append(y_offsets2[i])

        # Insert the zero value at the beginning
        rearranged_offsets.insert(0, 0.0)
        y_offsets = {i: rearranged_offsets[i - 1] for i in
                     range(1, max_instance + 1)}  # Map offsets to instance numbers

        create_optimized_positions(self, base_y_values, instance_dict, y_offsets, actions, action_transitions,
                                   file_offset, file_base, num_iterations, optimize_positions)

    def create_markers(self, actions, instance_dict, preferred_offset, preferred_base, measures_in_pathways, line_choice):
        """
        Creates markers for the pathways plot.

        Parameters:
        - actions: Dictionary of actions.
        - instance_dict: Dictionary mapping measures to their instances.
        - preferred_offset: Dictionary of preferred y-offsets.
        - preferred_base: Dictionary of preferred base y-values.
        - measures_in_pathways: Dictionary mapping pathways to their associated measures.

        Returns:
        - action_pairs: Dictionary for storing Begin and End coordinates by measure and instance.
        - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
        - preferred_dict_inv: Inverse dictionary of preferred base y-values.
        """
        # Create an inverse dictionary for preferred base y-values
        preferred_dict_inv = {v: k for k, v in preferred_base.items()}

        # Initialize a dictionary to store begin and end coordinates for each measure and instance
        action_pairs, data = create_marker_dictionary(self, actions, preferred_base, instance_dict, preferred_offset,
                                                      measures_in_pathways, line_choice)
        return action_pairs, data, preferred_dict_inv

    def manual_adjust_base_positions(self, original_base_positions, changing_positions, change_type):
        """
        Manually adjusts the base positions of measures.

        Parameters:
        - original_base_positions: Dictionary of original base positions.
        - changing_positions: Dictionary of positions to change.
        - change_type: Type of change ('swap' or 'new_order').

        Returns:
        - original_base_positions: Updated dictionary of base positions.
        """
        if change_type == 'swap':
            for change, change_with in changing_positions.items():
                original_base_positions[change], original_base_positions[change_with] = original_base_positions[
                                                                                            change_with], \
                                                                                        original_base_positions[change]
        if change_type == 'new_order':
            original_base_positions = changing_positions

        return original_base_positions

    def create_base_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                           measures_in_pathways, ylabels):
        """
        Creates the base figure for the pathways plot using Matplotlib.

        Parameters:
        - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
        - action_pairs: Dictionary for storing Begin and End coordinates by measure and instance.
        - action_transitions: List of action transitions.
        - x_offsets: Dictionary of x-offsets.
        - preferred_dict_inv: Inverse dictionary of preferred base y-values.
        - measures_in_pathways: Dictionary mapping pathways to their associated measures.
        - ylabels: String whether to add logos, names or numbers to the plot.

        Returns:
        - None
        """
        # Create a new figure and axis for plotting
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        # Generate the base figure and save it
        base_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv, measures_in_pathways,
                    ylabels)

    def create_base_figure_plotly(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv,
                                  measures_in_pathways, ylabels, filename):
        """
        Creates the base figure for the pathways plot using Plotly.

        Parameters:
        - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
        - action_pairs: Dictionary for storing Begin and End coordinates by measure and instance.
        - action_transitions: List of action transitions.
        - offsets: Dictionary of x-offsets.
        - preferred_dict_inv: Inverse dictionary of preferred base y-values.
        - measures_in_pathways: Dictionary mapping pathways to their associated measures.
        - ylabels: String whether to add logos, names or numbers to the plot.

        Returns:
        - None
        """
        # Generate the base figure and save it
        base_figure_plotly(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv,
                           measures_in_pathways, ylabels, filename)

    def pathways_change_plotly(self, data_new, action_pairs_new, action_transitions_new, data_old, action_pairs_old,
                               action_transitions_old, offsets, preferred_dict_inv, measures_in_pathways, ylabels, filename,
                               color='grey', ):
        """
        Creates a pathways change plot using Plotly.

        Parameters:
        - data_new: New pathways data for plotting.
        - action_pairs_new: New action pairs for pathways.
        - action_transitions_new: New action transitions.
        - data_old: Old pathways data for plotting.
        - action_pairs_old: Old action pairs for pathways.
        - action_transitions_old: Old action transitions.
        - offsets: Dictionary of x-offsets.
        - preferred_dict_inv: Inverse dictionary of preferred base y-values.
        - measures_in_pathways: Dictionary mapping pathways to their associated measures.
        - ylabels: String whether to add logos, names or numbers to the plot.
        - color: Color for the old pathways (default is 'grey').

        Returns:
        - None
        """
        # Generate the base figure and save it
        pathways_change_plotly(self, data_new, action_pairs_new, action_transitions_new, data_old, action_pairs_old,
                               action_transitions_old, offsets, preferred_dict_inv, measures_in_pathways, ylabels,
                               color, filename)

    def add_other_map(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv, measures_in_pathways,
                      ylabels, color='grey', alpha=0.8):
        """
        Adds another pathways map to the existing figure using Matplotlib.

        Parameters:
        - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
        - action_pairs: Dictionary for storing Begin and End coordinates by measure and instance.
        - action_transitions: List of action transitions.
        - x_offsets: Dictionary of x-offsets.
        - preferred_dict_inv: Inverse dictionary of preferred base y-values.
        - measures_in_pathways: Dictionary mapping pathways to their associated measures.
        - ylabels: String whether to add logos, names or numbers to the plot.
        - color: Color for the other pathways (default is 'grey').
        - alpha: Transparency level for the other pathways (default is 0.8).

        Returns:
        - None
        """
        other_figure(self, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv, measures_in_pathways,
                     ylabels, color, alpha)
