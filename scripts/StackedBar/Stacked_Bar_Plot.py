import pandas as pd
from scripts.helperfunctions.add_measure_buttons import add_measure_buttons
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV
from scripts.main_central_path_directions import LEGENDS_LOCATION_GITHUB
from scripts.helperfunctions.get_table_for_plot import get_table_for_plot
from scripts.StackedBar.get_change_between_old_and_new import get_change_between_old_and_new
from scripts.StackedBar.add_trace_one_bar import add_traces_oneBar
from scripts.StackedBar.add_custom_legend import add_custom_legend
import plotly.graph_objects as go  # Import Plotly's graph_objects module
from scripts.helperfunctions.add_line_breaks_axis_labels import add_line_breaks
import json

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def Stacked_Bar_Plot(df, risk_owner_hazard, sector_objectives, figure_title, df_interaction=None):
    # Load the dictionary from the JSON file
    with open(f'data/renamed_pathways/renamed_pathways_{risk_owner_hazard}.json', 'r') as json_file:
        replace_dict = json.load(json_file)
    invert_replace_dict = {v: int(k) for k, v in replace_dict.items()}

    # Replace old values with new values in the 'risk_owner_hazard' column
    df[risk_owner_hazard] = df[risk_owner_hazard].replace(invert_replace_dict)

    # Plot no interaction plot
    benchmark_values = df[df[risk_owner_hazard] == 0]

    pivot_df, pivot_text_df = get_table_for_plot(df, risk_owner_hazard)
    _, pivot_text_benchmark = get_table_for_plot(benchmark_values, risk_owner_hazard)


    plot_df = pivot_df
    text_df = pivot_text_df
    text_df_benchmark = pivot_text_benchmark
    plot_objectives = sector_objectives
    groupname = 'no interactions'

    if df_interaction is not None:
        df_interaction[risk_owner_hazard] = df_interaction[risk_owner_hazard].replace(invert_replace_dict)
        print('Interaction added')
        ## UNTIL I UPDATED THE CODE ##
        df_interaction = pd.concat([df_interaction, benchmark_values], ignore_index=True)
        # Replace old values with new values in the 'risk_owner_hazard' column
        print('## UNTIL I UPDATED THE CODE ## CHECK AFTER!!!!')
        # Benchmark values for interaction
        interaction_benchmark_values = df.copy()
        pivot_interaction, pivot_interaction_text = get_table_for_plot(df_interaction, risk_owner_hazard)
        _, pivot_text_interaction_benchmark = get_table_for_plot(interaction_benchmark_values, risk_owner_hazard)

        pivot_interaction[risk_owner_hazard] = pivot_interaction[risk_owner_hazard].replace(invert_replace_dict)
        pivot_interaction_text[risk_owner_hazard] = pivot_interaction_text[risk_owner_hazard].replace(invert_replace_dict)
        pivot_text_interaction_benchmark[risk_owner_hazard] = pivot_text_interaction_benchmark[risk_owner_hazard].replace(invert_replace_dict)


        # Calculate differences and add them as new columns
        pivot_interaction, objectives_with_interactions = get_change_between_old_and_new(pivot_df,
                                                                                         pivot_interaction,
                                                                                         sector_objectives,
                                                                                         risk_owner_hazard)
        pivot_interaction_text, _ = get_change_between_old_and_new(pivot_text_df,
                                                                   pivot_interaction_text,
                                                                   sector_objectives, risk_owner_hazard,
                                                                   normalized=False)

        plot_df = pivot_interaction

        plot_df.index = plot_df[risk_owner_hazard]
        text_df = pivot_interaction_text
        text_df_benchmark = pivot_interaction_text
        text_df.index = text_df[risk_owner_hazard]
        text_df_benchmark.index = text_df_benchmark[risk_owner_hazard]
        plot_objectives = objectives_with_interactions

        groupname = 'with interactions'

    fig = go.Figure()

    initial_traces, static_legend_entries = add_traces_oneBar(
        plot_objectives,
        sector_objectives,
        plot_df, text_df,
        text_df_benchmark,
        risk_owner_hazard,
        offsetgroup=0, legend_entries={}, groupname_base=groupname)
    for trace in initial_traces:
        fig.add_trace(trace)

    # Update the layout to make the bars grouped
    fig.update_layout(
        barmode='relative',
        legend_traceorder='grouped',  # Ensures the legends are sorted
    # legend = dict(groupclick="toggleitem")
    )

    fig = add_custom_legend(fig, static_legend_entries, risk_owner_hazard,  x_start=.75, y_start=.15, y_step=-0.04)
    fig.add_annotation(
        x=0.0,  # Adjust this value to move the label left or right
        y=0.625,  # Adjust this value to move the label up or down
        text=f'{ROH_DICT_INV[risk_owner_hazard]} pathway options',  # Your y-axis label text here
        showarrow=False,
        xref='paper',
        yref='paper',
        textangle=-90,  # Rotate text for vertical orientation
        font=dict(size=14),  # Adjust font size as needed
        align='center'
    )
    x_axis_range = [0, len(sector_objectives) + 1]
    # # Customize the x-tick labels
    fig.update_xaxes(
        tickvals=list(range(x_axis_range[0], x_axis_range[1])),
        ticktext=list(range(x_axis_range[0], x_axis_range[1]))
    )

    # Update both axes and add annotations in a single update_layout call
    fig.update_layout(
        # X-Axis configuration
        xaxis=dict(
            showticklabels=False,  # Hide x-tick labels
            title_text='The shorter the bar(s), the better',  # Remove x-axis title
            range=x_axis_range,
            domain=[0.25, 1]  # Adjust x-axis domain
        ),
        yaxis=dict(
            domain=[0.25, .93]  # Adjust x-axis domain
        ),
    )

    # # Add annotations
    # fig.add_annotation(
    #     x=.1, y=.82,
    #     text="<b>The shorter the bar, the better</b>",
    #     showarrow=True,
    #     arrowhead=2,
    #     ax=40,
    #     ay=0,
    #     yshift=-50,
    #     xanchor='left',
    #     # bordercolor="red",
    #     # borderwidth=3  # Set the border width to be thick
    # )

    # # Add rectangle shape to encompass the annotation and arrow
    # fig.add_shape(
    #     type="rect",
    #     x0=0.05, y0=7.55,
    #     x1=1, y1=7.8,  # Adjust these coordinates to fit the annotation and arrow
    #     xref="x",
    #     yref="y",
    #     line=dict(color="red", width=3)
    # )
    if df_interaction:
        # Update the layout to adjust the legend position
        fig.update_layout(
            legend=dict(
                y=0.93,  # Position the legend at 90% of the plot's height (from the bottom)
                yanchor='top',  # Align the top of the legend box with the y position
                x=0.81,  # Optionally adjust the horizontal position
                xanchor='left'  # Align the left of the legend box with the x position
            ))

        # Add a shape for the box with transparent body color and red line
        fig.add_shape(
            type="rect",
            x0=.81, y0=0.8 if df_interaction is None else 0.92, x1=1, y1=.93,  # Coordinates for the box
            xref="paper",
            yref="paper",
            layer='above',
            line=dict(color="red", width=2),  # Red line with specified width
            fillcolor="rgba(0, 0, 0, 0)"  # Transparent body color
        )

        # Add annotation for the text
        fig.add_annotation(
            x=.83, y=.92,  # Position of the text (top left corner of the box)
            text="<b>Click to toggle the<br>effects of interactions</b>",
            showarrow=False,
            xanchor="left",
            yanchor="top",
            xref="paper",
            yref="paper",
            font=dict(color="black", size=12)  # Adjust the font size and color as needed
        )
    else:
        fig.update_layout(
            showlegend=False
            )
    # Switch back to add right legends
    # print(replace_dict)
    plot_df[risk_owner_hazard] = plot_df[risk_owner_hazard].astype(str).replace(replace_dict)

    fig = add_measure_buttons(fig, plot_df[risk_owner_hazard].astype(str),
                              risk_owner_hazard, x_start=0.04)

    # Add an image under the legend to the left
    fig.add_layout_image(
        dict(
            source=f'{LEGENDS_LOCATION_GITHUB}/{risk_owner_hazard}_full_legend.png',
            # Replace with your image URL or path
            x=.0,  # Adjust x position (slightly right of the legend)
            y=.0,  # Adjust y position
            xref="paper",
            yref="paper",
            sizex=.8,  # Adjust size of the image
            sizey=.8,
            xanchor="left",
            yanchor="bottom"
        )
    )

    fig.update_layout(
        # Title and positioning
        title={'text': add_line_breaks(figure_title, 50), 'y': .95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom'},
        title_font_size=18,
        font_size=14,

        # Custom margins
        margin=dict(l=5, r=5, t=30, b=5),
        # Fixed dimensions for the plot
        width=667,  # Width set to 1300 pixels
        height=567,  # Height set to 600 pixels
        autosize=False,  # Disable autosizing to use the specified width and height

    )

    fig.show()
    print(error)
    return fig