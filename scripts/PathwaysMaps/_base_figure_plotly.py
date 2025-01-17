import numpy as np
import plotly.graph_objects as go
from scripts.PathwaysMaps._find_integers import find_first_and_second_integers
from scripts.map_system_parameters import INVERTED_MEASURE_NUMBERS, REPLACING_MEASURE
from scripts.main_central_path_directions import LEGENDS_LOCATION_GITHUB
from scripts.PathwaysMaps.jsonscript import HOVER_JS
from scripts.main_central_path_directions import DIRECTORY_MEASURE_LOGOS_GITHUB
import json

max_line_offset = 0.2
def base_figure_plotly(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv, measures_in_pathways, planning_horizon, ylabels,risk_owner_hazard, filename):
    """
    Creates the base figure for the pathways map using Plotly.

    Parameters:
    - self: The class instance containing various configurations.
    - data: Dict containing plotting data organized by measure.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - action_transitions: List of transitions between actions.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.

    Returns:
    - fig: The Plotly figure with the base pathways map.
    """
    line_width_marker = 3
    size_marker = 15
    line_width_line = 3

    fig = go.Figure()

    # Add horizontal lines to the plot
    fig = add_horizontal_lines(fig, action_pairs, measures_in_pathways, self.line_choice, self.replacing_measure, self.measure_colors)

    # Add vertical lines to the plot
    fig = add_vertical_lines(fig, action_transitions, action_pairs, measures_in_pathways, offsets, line_width_line, self.measure_colors)

    # Add markers to the plot
    fig = add_actions(fig, data, line_width_marker, size_marker)

    # Optionally add measure logos to the plot
    if ylabels == 'logos':
        fig = add_measure_buttons_plotly(fig, preferred_dict_inv)

    # Update layout with titles and hover mode
    fig.update_layout(
        title='Base Pathways Map',
        xaxis_title='Years',
        yaxis_title='',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=30, r=5, t=30, b=20),
        xaxis=dict(
            domain=[0, .6]  # Adjust x-axis domain
        ),
        width=1280,  # Width set to 1300 pixels
        height=600,  # Height set to 600 pixels


        autosize=False,  # Disable autosizing to use the specified width and height
    )
    fig.update_xaxes({'range': (planning_horizon[0], planning_horizon[1]), 'autorange': False})

    # Add an image under the legend to the left
    fig.add_layout_image(
        dict(
            source=f'{LEGENDS_LOCATION_GITHUB}/vertical_{risk_owner_hazard}_full_legend.png',
            # Replace with your image URL or path
            x=.94,  # Adjust x position (slightly right of the legend)
            y=.5,  # Adjust y position
            xref="paper",
            yref="paper",
            sizex=.7,  # Adjust size of the image
            sizey=.7,
            xanchor="right",
            yanchor="middle"
        )
    )
    # Update the y-axis to hide the y-ticks
    fig.update_yaxes(showticklabels=False)

    # Write the plot to an HTML file and append custom JavaScript for hover behavior
    fig.write_html(f'{filename}.html', include_plotlyjs='cdn')
    with open(f'{filename}.html', 'a') as f:
        f.write(HOVER_JS)

    # Convert the figure to JSON
    fig_json = fig.to_plotly_json()
    # Add the custom JavaScript to the JSON structure
    fig_json['custom_js'] = HOVER_JS

    with open(f'{filename}.json', 'w') as f:
        json.dump(fig_json, f)

    return fig

def pathways_change_plotly(self, data_new, action_pairs_new, action_transitions_new, data_old, action_pairs_old, action_transitions_old, offsets, preferred_dict_inv, measures_in_pathways_new, measures_in_pathways_old, planning_horizon,risk_owner_hazard, ylabels, color, filename):
    """
    Creates the pathways change figure using Plotly, highlighting changes between two scenarios for the same set of pathways.

    Parameters:
    - self: The class instance containing various configurations.
    - data_new: Dict containing plotting data to be highlighed organized by measure.
    - action_pairs_new: Dict containing the start and end coordinates of actions to be highlighed.
    - action_transitions_new: List of transitions between actions to be highlighed.
    - data_old: Dict containing plotting data for reference organized by measure.
    - action_pairs_old: Dict containing the start and end coordinates of actions for reference.
    - action_transitions_old: List of transitions between actions for reference.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.

    Returns:
    - fig: The Plotly figure with the pathways change map.
    """
    line_width_marker = 3
    size_marker = 15
    line_width_line = 3

    fig = go.Figure()

    # Add old pathways (colored grey)
    fig = add_horizontal_lines(fig, action_pairs_old, measures_in_pathways_old, self.line_choice, self.replacing_measure, self.measure_colors, color, other_pathways=True)
    fig = add_vertical_lines(fig, action_transitions_old, action_pairs_old, measures_in_pathways_old, offsets, line_width_line, self.measure_colors, color, other_pathways=True)

    # Add new pathways
    fig = add_horizontal_lines(fig, action_pairs_new, measures_in_pathways_new, self.line_choice, self.replacing_measure, self.measure_colors)
    fig = add_vertical_lines(fig, action_transitions_new, action_pairs_new, measures_in_pathways_new, offsets, line_width_line, self.measure_colors)

    # Add markers for old and new pathways
    fig = add_actions(fig, data_old, line_width_marker, size_marker, color, other_pathways=True)
    fig = add_actions(fig, data_new, line_width_marker, size_marker)

    # Optionally add measure logos to the plot
    if ylabels == 'logos':
        fig = add_measure_buttons_plotly(fig, preferred_dict_inv)

    # Update layout with titles and hover mode
    fig.update_layout(
        title='Pathways Map with interactions and base (grey)',
        xaxis_title='Years',
        yaxis_title='',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=30, r=5, t=30, b=20),
        xaxis=dict(
            domain=[0, .6]  # Adjust x-axis domain
        ),
        width=1280,  # Width set to 1300 pixels
        height=600,  # Height set to 600 pixels


        autosize=False,  # Disable autosizing to use the specified width and height
    )
    fig.update_xaxes({'range': (planning_horizon[0], planning_horizon[1]), 'autorange': False})
    # Update the y-axis to hide the y-ticks
    fig.update_yaxes(showticklabels=False)

    # Add an image under the legend to the left
    fig.add_layout_image(
        dict(
            source=f'{LEGENDS_LOCATION_GITHUB}/vertical_{risk_owner_hazard}_full_legend.png',
            # Replace with your image URL or path
            x=.94,  # Adjust x position (slightly right of the legend)
            y=.5,  # Adjust y position
            xref="paper",
            yref="paper",
            sizex=.8,  # Adjust size of the image
            sizey=.8,
            xanchor="right",
            yanchor="middle"
        )
    )

    # Write the plot to an HTML file and append custom JavaScript for hover behavior
    fig.write_html(f'{filename}.html', include_plotlyjs='cdn')
    with open(f'{filename}.html', 'a') as f:
        f.write(HOVER_JS)

    return fig

def add_actions(fig, data, line_width_marker, size_marker, color='grey', other_pathways=False):
    """
    Adds action markers to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add markers to.
    - data: Dict containing plotting data organized by measure.
    - line_width_marker: Width of the marker lines.
    - size_marker: Size of the markers.
    - other_pathways: Boolean indicating whether the markers belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added action markers.
    """
    for measure, points in data.items():
        for point in points:
            x, y = point[0]

            symbol = 'circle'
            facecolor = color if other_pathways else 'white' if point[3] == 'w' else point[3]

            marker = dict(
                symbol=symbol,
                size=size_marker,
                color=facecolor,
                line=dict(color=color if other_pathways else point[2], width=line_width_marker)
            )

            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=marker,
                showlegend=False,
                customdata=[point[4]],  # Full list of groups for each point without additional nesting
                hovertext=f'Pathways{point[4]}'  # Display the pathways correctly
            ))
    return fig

def add_horizontal_lines(fig, action_pairs, measures_in_pathways, line_choice, replacing_measure, measure_colors, color='grey',  other_pathways=False):
    """
    Adds horizontal lines to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add lines to.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - measures_in_pathways: Dict of measures in each pathway.
    - line_choice: Indicating whether different pathways are drawn with unique lines for active measures or just overlaid
    - replacing_measure: Dict of measures being replaced.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added horizontal lines.
    """
    line_width_line = 2

    if line_choice == 'pathways_and_unique_lines':
        # Plot current measure
        coords = action_pairs[('0', '0')]
        begin_coords = coords['Begin']
        end_coords = coords['End']

        fig.add_trace(go.Scatter(
            x=[begin_coords[0], end_coords[0]],
            y=[begin_coords[1], end_coords[1]],
            mode='lines',
            line=dict(color=color if other_pathways else measure_colors.get('0', 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
            showlegend=False,
            customdata=[key for key, array in measures_in_pathways.items()]
        ))


        for pathway, measures in measures_in_pathways.items():
            old_keys = []
            measures_split = [tuple(item.replace(']', '').split('[')) for item in measures]
            relevant_measures = {action_pairs[measure_instance]['Begin'][0]: measure_instance for measure_instance in measures_split if len(measure_instance) > 1}
            sorted_years = sorted(relevant_measures)

            # add lines based on increasing years
            for year in sorted_years:
                measure_instance = relevant_measures[year]
                coords = action_pairs[measure_instance]
                begin_coords = coords['Begin']
                end_coords = coords['End']
                measure, instance = measure_instance
                customdata = [key for key, array in measures_in_pathways.items() if f'{measure}[{instance}]' in array or (measure == '0' and f'{measure}' in array)]
                fig.add_trace(go.Scatter(
                    x=[begin_coords[0], end_coords[0]],
                    y=[begin_coords[1], end_coords[1]],
                    mode='lines',
                    line=dict(color=color if other_pathways else measure_colors.get(measure, 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
                    showlegend=False,
                    customdata=customdata
                ))

                # if previous measures have not been replaced, plot a line for this as well between
                # given coordinates
                max_number_lines = len(old_keys)
                if max_number_lines == 1:
                    offset_lines = max_line_offset * .5
                else:
                    offset_lines = max_line_offset
                y_offsets1 = np.linspace(0, offset_lines, int(np.floor(max_number_lines * 2 / 2)) + 1)
                y_offsets2 = np.linspace(-offset_lines, 0, int(np.ceil(max_number_lines * 2 / 2)) + 1)[::-1]
                # Initialize the rearranged list
                rearranged_offsets = []

                # Interleave the values from y_offsets1 and y_offsets2
                for i in range(1, len(y_offsets2)):
                    rearranged_offsets.append(y_offsets1[i])
                    rearranged_offsets.append(y_offsets2[i])
                # Insert the zero value at the beginning
                rearranged_offsets.insert(0, 0.0)

                for i, previous in enumerate(old_keys):
                    if previous not in replacing_measure.get(measure, []):
                        ybegin_coords = begin_coords[1] + rearranged_offsets[i+1]
                        yend_coords = end_coords[1] + rearranged_offsets[i+1]
                        fig.add_trace(go.Scatter(
                            x=[begin_coords[0], end_coords[0]],
                            y=[ybegin_coords, yend_coords],
                            mode='lines',
                            line=dict(color=color if other_pathways else measure_colors.get(previous, 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
                            showlegend=False,
                            customdata=customdata,
                            hovertext=customdata
                        ))
                old_keys.append(measure)
    else:
        for (measure, instance), coords in action_pairs.items():
            customdata = [key for key, array in measures_in_pathways.items() if f'{measure}[{instance}]' in array or (measure == '0' and f'{measure}' in array)]
            if 'Begin' in coords and 'End' in coords:
                begin_coords = coords['Begin']
                end_coords = coords['End']
                fig.add_trace(go.Scatter(
                    x=[begin_coords[0], end_coords[0]],
                    y=[begin_coords[1], end_coords[1]],
                    mode='lines',
                    line=dict(color=color if other_pathways else measure_colors.get(measure, 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
                    showlegend=False,
                    customdata=customdata,
                    hovertext=customdata
                ))
    return fig

def add_vertical_lines(fig, action_transitions, action_pairs, measures_in_pathways, offsets, line_width_line, measure_colors, color='grey',  other_pathways=False):
    """
    Adds vertical lines to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add lines to.
    - action_transitions: List of transitions between actions.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - measures_in_pathways: Dict of measures in each pathway.
    - offsets: Dict of offsets for measures.
    - line_width_line: Width of the lines.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added vertical lines.
    """
    for transition in action_transitions:
        if isinstance(transition[2], int):
            # Skip horizontal lines
            continue
        else:
            start_measure, start_instance = find_first_and_second_integers(transition[0])
            end_measure, end_instance = find_first_and_second_integers(transition[2])
            end_x_pos = transition[1]

            customdata = [key for key, array in measures_in_pathways.items() if f'{end_measure}[{end_instance}]' in array or (end_measure == '0' and f'{end_measure}' in array)]

            if start_measure != '0':
                group_offset = offsets.get(start_measure, 0)
                end_x_pos += group_offset

            if (start_measure, start_instance) in action_pairs:
                if 'Begin' in action_pairs[(start_measure, start_instance)]:
                    start_y_pos = action_pairs[(start_measure, start_instance)]['Begin'][1]
                    end_y_pos = action_pairs[(end_measure, end_instance)]['End'][1]
                    fig.add_trace(go.Scatter(
                        x=[end_x_pos, end_x_pos],
                        y=[start_y_pos, end_y_pos],
                        mode='lines',
                        line=dict(color=color if other_pathways else measure_colors.get(start_measure, 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
                        showlegend=False,
                        customdata=customdata,
                        hovertext=customdata
                    ))
    return fig

def add_measure_buttons_plotly(fig, preferred_dict_inv):
    """
    Adds measure buttons (logos) to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add buttons to.
    - preferred_dict_inv: Dict for measure button mappings.

    Returns:
    - fig: The Plotly figure with added measure buttons.
    """
    for key, element in preferred_dict_inv.items():
        img_path = f'{DIRECTORY_MEASURE_LOGOS_GITHUB}/colorized/{INVERTED_MEASURE_NUMBERS[int(preferred_dict_inv[key])]}.png'

        fig.add_layout_image(
            dict(
                source=img_path,
                xref="paper",  # Use "paper" for relative positioning
                yref="y",  # Use axis ID for aligning with specific ticks
                x=0,  # Adjust this value to position the image on the x-axis
                y=key,  # Align with a specific y-axis tick label
                sizex=0.7,
                sizey=0.7,
                xanchor="left",
                yanchor="middle",
            ),
        )
    return fig
