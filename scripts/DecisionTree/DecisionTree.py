import pandas as pd
import plotly.graph_objects as go
from scripts.map_system_parameters import MEASURE_DICT, MEASURE_EXPL
from scripts.design_choices.main_dashboard_design_choices import MEASURE_COLORS, MEASURE_NUMBERS

from scripts.DecisionTree.assign_group_numbers import assign_group_numbers
from scripts.DecisionTree.calculate_postion_measure import calculate_position_measure
import pathlib
import json

def decision_tree(input_file, sector, button_path, filter_sector):
    # Convert sequences to DataFrame
    df = pd.read_csv(input_file, names=['Measure 1', 'Measure 2', 'Measure 3', 'Measure 4'])
    df = df.loc[filter_sector[1:]]

    # Assign group numbers for each depth
    for depth in range(1, 5):
        df = assign_group_numbers(df, depth)

    df_sorted = df.copy()
    # Initialize the Position_measure_4 column with the values from 'Group up to Measure 4'
    df_sorted['Position_measure_4'] = df_sorted['Group up to Measure 4']

    # Calculate Position_measure_3
    df_sorted = calculate_position_measure(df_sorted, 3, 'Group up to Measure 3')

    # Calculate Position_measure_2
    df_sorted = calculate_position_measure(df_sorted, 2, 'Group up to Measure 2')

    # Calculate Position_measure_1 similarly, but since it's the first measure, it refers to itself for uniqueness
    df_sorted = calculate_position_measure(df_sorted, 1, 'Group up to Measure 1')

    df_sorted['Position_measure_0'] = (df_sorted['Position_measure_1'].min() + df_sorted['Position_measure_1'].max()) / 2
    df_sorted[f'Group up to Measure 0'] = 1

    # Preparing data for the scatter plot
    x_positions = []
    y_positions = []
    image_paths = []
    measure_names = []
    measure_expl = []
    pw_number = []
    colors = []


    # Iterating over the Position_measure columns to collect x and y positions for the scatter plot
    for i in range(5):
        column_name = f'Position_measure_{i}'
        x_positions.extend([i] * len(df_sorted))  # X position based on the measure number
        y_positions.extend(df_sorted[column_name])  # Y position from the column values
        if i == 0:
            image_paths.extend([f'{button_path}/no_measure.png' for _ in df_sorted.index])
            measure_names.extend([f'No new measure' for _ in df_sorted.index])
            measure_expl.extend([MEASURE_EXPL['no_measure'] for _ in df_sorted.index])
            pw_number.extend(df_sorted.index)
            colors.extend([MEASURE_COLORS['0'] for _ in df_sorted.index])
        else:
            column_name = f'Measure {i}'
            image_paths.extend(f'{button_path}/{x}.png' for x in df_sorted[column_name])
            measure_names.extend([MEASURE_DICT[x] for x in df_sorted[column_name]])
            measure_expl.extend([MEASURE_EXPL[x] for x in df_sorted[column_name]])
            pw_number.extend(df_sorted.index)
            colors.extend(MEASURE_COLORS[str(MEASURE_NUMBERS[x])] for x in df_sorted[column_name])

    # Creating a DataFrame with the correct structure
    df_test = pd.DataFrame({

        'X_Positions': x_positions,
        'Y_Positions': y_positions,
        'Image_Paths': image_paths,
        'Measure_Names': measure_names,
        'Measure_Explanation': measure_expl,
        'Color': colors
    })

    df_pathways = pd.DataFrame({
        'Pathway': pw_number,
        'X_Positions': x_positions,
        'Y_Positions': y_positions,
    })

    print(df_pathways)
    # store new pathway numbers
    new_pathway_numbers = {}
    new_pathway_numbers[0] = 0
    unique_pathways = df_pathways[df_pathways.X_Positions == 4].sort_values('Y_Positions')
    for e, p in enumerate(unique_pathways['Pathway']):
        new_pathway_numbers[e+1] = p

    # Convert and write JSON object to file
    with open(f"data/renamed_pathways/renamed_pathways_{sector}.json", "w") as outfile:
        json.dump(new_pathway_numbers, outfile)

    # Get the index of the maximum 'X_Positions' within each 'Pathway' group
    max_indices = df_pathways.groupby('Pathway')['X_Positions'].idxmax()

    # Filter the DataFrame using these indices
    df_pathways = df_pathways.loc[max_indices]

    position_dict = {row['Y_Positions']: str(int(row['Pathway'])) for index, row in df_pathways.iterrows()}

    fig = go.Figure()
    # Creating the scatter plot with Plotly
    fig.add_trace(go.Scatter(x=df_test['X_Positions'], y=df_test['Y_Positions'],
                     text=df_test['Measure_Names'],
                     mode='markers',  # Only markers, no lines
                     # This can be useful if you want simple hover text, but we'll use hovertemplate instead
                     hovertemplate=
                     "<b>Measure Name: %{text}</b><br>" +
                     "<b>Explanation:</b><br>%{customdata}<br>" +
                     "</span>" +
                     "<extra></extra>",
                     customdata=df_test['Measure_Explanation'],
                    marker=dict(
                        color=df_test['Color'],  # Use the color column for marker colors
                        size=10)  # Adjust marker size as needed
                             ))

    # Adding vertical lines based on the logic described
    for i in range(4):  # Only up to measure 3 since we look ahead by one
        current_column = f'Group up to Measure {i}'
        next_column = f'Group up to Measure {i + 1}'
        unique_groups = df_sorted[current_column].unique()

        for group in unique_groups:
            group_rows = df_sorted[df_sorted[current_column] == group]
            next_measure_groups = group_rows[next_column].unique()

            if len(next_measure_groups) > 1:
                min_pos = group_rows[f'Position_measure_{i + 1}'].min()
                max_pos = group_rows[f'Position_measure_{i + 1}'].max()
                fig.add_shape(type='line',
                              x0=i + 0.5, y0=min_pos,
                              x1=i + 0.5, y1=max_pos,
                              line=dict(color='gray', width=2)
                              )

    # Adding horizontal lines for both identical and different y-values between measures
    drawn_lines = set()  # Initialize a set to keep track of drawn lines
    only_necessary = df_sorted.drop_duplicates(subset=[f'Position_measure_{k}' for k in range(4)])

    for index, row in only_necessary.iterrows():
        for i in range(4):  # Up to measure 3 to look ahead to measure 4
            current_pos = row[f'Position_measure_{i}']
            next_pos = row[f'Position_measure_{i + 1}']

            line_part0 = (i, current_pos, i+1, current_pos)
            # Define line coordinates for horizontal line part 1
            line_part1 = (i, current_pos, i + 0.5, current_pos)
            # Define line coordinates for horizontal line part 2
            line_part2 = (i + 0.5, next_pos, i + 1, next_pos)

            if current_pos == next_pos:
                if line_part0 not in drawn_lines:
                    fig.add_shape(type='line', x0=line_part0[0], y0=line_part0[1], x1=line_part0[2], y1=line_part0[3],
                                  line=dict(color='gray', width=2), layer='below')
                    drawn_lines.add(line_part0)  # Mark this line as drawn
            # Draw the first part of the horizontal line if it hasn't been drawn
            else:
                if line_part1 not in drawn_lines:
                    fig.add_shape(type='line', x0=line_part1[0], y0=line_part1[1], x1=line_part1[2], y1=line_part1[3],
                                  line=dict(color='gray', width=2), layer='below')
                    drawn_lines.add(line_part1)  # Mark this line as drawn

                # Draw the second part of the horizontal line if it hasn't been drawn
                if line_part2 not in drawn_lines:
                    fig.add_shape(type='line', x0=line_part2[0], y0=line_part2[1], x1=line_part2[2], y1=line_part2[3],
                                  line=dict(color='gray', width=2), layer='below')
                    drawn_lines.add(line_part2)  # Mark this line as drawn
    for i, row in df_test.iterrows():
        fig.add_layout_image(
            source=row['Image_Paths'],
            # URL or path to your image
            xref="x",  # Use "paper" for positioning relative to the plot area
            yref="y",  # Use "paper" for positioning relative to the plot area
            x=row['X_Positions'],  # X-coordinate position
            y=row['Y_Positions'],  # Y-coordinate position
            sizex=.85,  # Adjust size as needed
            sizey=.85,  # Adjust size as needed
            xanchor="center",
            yanchor="middle",
            layer="above"  # Place the image below or above the data
        )


    # Update layout to configure axes and labels
    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            side='right',  # Position y-axis on the right side
            tickmode='array',
            tickvals=[key for key in position_dict.keys()],  # Ensure there's a tickval for each ticktext
            ticktext=[key for key in position_dict.keys()],
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(5)],
            ticktext=['' if numb == 0 else f'{numb}' for numb in range(5)],
            showgrid=False
        ),
        title={
            'text': 'Alternative Pathways and their Measure Sequences',
            'y': 0.98,  # Position the title a bit above the plot area
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Measure Number",
        yaxis_title="Alternative Pathways",
        plot_bgcolor="white",
        autosize=False,
        font=dict(
                size=14,
                ),
        width=1290,
        height=567,
        margin=dict(l=30, r=5, t=30, b=20),
    )
    pathlib.Path(f'figures/decision_tree/').mkdir(parents=True, exist_ok=True)
    fig.write_html(f"figures/decision_tree/alternative_pathways_{sector}.html")
    fig.write_json(f"figures/decision_tree/alternative_pathways_{sector}.json")