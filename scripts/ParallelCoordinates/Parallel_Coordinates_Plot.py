from scripts.map_system_parameters import AXIS_LABELS
from scripts.design_choices.main_dashboard_design_choices import COLORSCALE_PCP,COLORSCALE_NAMES
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV,ROH_DICT, RANGE
from scripts.ParallelCoordinates.make_thicker_lines import make_thicker_lines
from scripts.helperfunctions.add_line_breaks_axis_labels import add_line_breaks
from scripts.ParallelCoordinates.create_custom_colorscale import create_custom_colorscale
from scripts.ParallelCoordinates.generate_ticks import generate_ticks

import plotly.graph_objects as go
import pandas as pd
import json

def Parallel_Coordinates_Plot(df, risk_owner_hazard, figure_title, performance_metric, df_interaction=None):
    if df_interaction is None:
        pivot_df = df.pivot_table(
            index=[risk_owner_hazard],
            columns='objective_parameter',
            values='Value',
            aggfunc='sum'
        )
        reset_pivot = pivot_df.reset_index()
        reset_pivot['Color'] = reset_pivot[risk_owner_hazard]
    else:
        pivot_df1 = df.pivot_table(
            index=[risk_owner_hazard],
            columns='objective_parameter',
            values='Value',
            aggfunc='sum'
        )
        reset_pivot1 = pivot_df1.reset_index()
        reset_pivot1['Color'] = 1000

        pivot_df2 = df_interaction.pivot_table(
            index=[risk_owner_hazard],
            columns='objective_parameter',
            values='Value',
            aggfunc='sum'
        )
        reset_pivot2 = pivot_df2.reset_index()
        reset_pivot2['Color'] = reset_pivot2[risk_owner_hazard]

        reset_pivot = pd.concat([reset_pivot1, reset_pivot2], ignore_index=True)

    objective_parameters = df['objective_parameter'].unique()
    objective_parameters = sorted(objective_parameters, key=lambda x: 'Cost' not in x)

    new_order = [risk_owner_hazard, *objective_parameters, 'Color']
    reset_pivot = reset_pivot[new_order]

    ## Rename pathways in sequential order
    # Load the dictionary from the JSON file
    with open(f'data/renamed_pathways/renamed_pathways_{risk_owner_hazard}.json', 'r') as json_file:
        replace_dict = json.load(json_file)
    invert_replace_dict = {v: int(k) for k, v in replace_dict.items()}

    # Replace old values with new values in the 'risk_owner_hazard' column
    reset_pivot[risk_owner_hazard] = reset_pivot[risk_owner_hazard].replace(invert_replace_dict)

    reset_pivot = reset_pivot.rename(columns=AXIS_LABELS)
    reset_pivot = reset_pivot.rename(columns=ROH_DICT_INV)

    dimensions_to_modify = df.objective_parameter.unique()
    dimensions_to_modify = [ROH_DICT_INV[risk_owner_hazard]] + [AXIS_LABELS[dim] for dim in dimensions_to_modify]

    combined_data = make_thicker_lines(reset_pivot, dimensions_to_modify, 0.005, 50)
    # combined_data = reset_pivot.copy()

    labels = [col for col in combined_data.columns if col not in ['Color', 'performance_metric']]
    labels_with_linebreaks = {v: add_line_breaks(v) for v in labels}

    combined_data_sorted = combined_data.sort_values(by=['Color'], ascending=False).reset_index(drop=True)

    dimensions = [
        dict(range=RANGE[col],
             label=labels_with_linebreaks[col],
             values=combined_data_sorted[col],
)
        for col in combined_data_sorted.columns if col not in ['Color', 'performance_metric']
    ]

    color_values, custom_colorscale = create_custom_colorscale(combined_data_sorted)

    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=color_values,
            colorscale=custom_colorscale,
        ),
        dimensions=dimensions,
        unselected=dict(line=dict(color='lightgrey', opacity=0.0)),
        domain=dict(
            x=[0.12, 0.9],  # Adjust the horizontal domain (left, right)
            y=[0.02, 0.75]  # Adjust the vertical domain (bottom, top)
        )

    ))

    # fig.update_traces(
    #     dimensions=[
    #         {**d,
    #          "tickvals": generate_ticks(d['range'][0], d['range'][1], d['range'][1]+1 if d['label'] in list(ROH_DICT.keys()) else int(d['range'][1]/10)+1, 1 if d['label'] in list(ROH_DICT.keys()) else 10)[0],
    #         "ticktext": generate_ticks(d['range'][0], d['range'][1], d['range'][1]+1 if d['label'] in list(ROH_DICT.keys()) else int(d['range'][1]/10)+1, 1 if d['label'] in list(ROH_DICT.keys()) else 10)[1]
    #         }
    #         for i, d in enumerate(fig.to_dict()["data"][0]["dimensions"])
    #     ]
    # )
    fig.update_traces(
        dimensions=[
            {**d,
             "tickvals": generate_ticks(d['range'][0], d['range'][1],
                                        d['range'][1] + 1 if d['label'] in list(ROH_DICT.keys()) else int(
                                            d['range'][1] / 10) + 1, 1 if d['label'] in list(ROH_DICT.keys()) else 10)[
                 0],
             "ticktext": generate_ticks(0 if d['label'] in list(ROH_DICT.keys()) else d['range'][0], RANGE[d['label']][1] if d['label'] in list(ROH_DICT.keys()) else d['range'][1],
                                        RANGE[d['label']][1] + 1 if d['label'] in list(ROH_DICT.keys()) else int(
                                            d['range'][1] / 10) + 1, 1 if d['label'] in list(ROH_DICT.keys()) else 10)[
                 1]
             }
            for i, d in enumerate(fig.to_dict()["data"][0]["dimensions"])
        ]
    )

    # Add scatter traces for the legend dynamically
    unique_colors = combined_data_sorted['Color'].unique()
    for scale_value, color in COLORSCALE_PCP:
        if scale_value in unique_colors:
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color=color),
                legendgroup=f'Group {scale_value}', showlegend=True, name=f'{COLORSCALE_NAMES[scale_value]}'
            ))


    # Add a shape for visual emphasis on the first axis
    fig.add_shape(
        type="rect",  # Add a rectangle shape
        x0=0, x1=0.24,  # Span a small range around the first axis
        y0=0, y1=.9,
        xref="paper", yref="paper",  # Reference the entire figure's dimensions
        fillcolor="lightgrey",  # Choose a subtle fill color
        opacity=0.5,  # Make the fill semi-transparent
        layer="below",  # Ensure the shape is below the data lines
        line_width=0,
    )

    # Add a shape for visual emphasis on the other axis
    fig.add_shape(
        type="rect",  # Add a rectangle shape
        x0=0.26, x1=1,  # Span a small range around the first axis
        y0=0, y1=.9,
        xref="paper", yref="paper",  # Reference the entire figure's dimensions
        fillcolor="lightgrey",  # Choose a subtle fill color
        opacity=0.5,  # Make the fill semi-transparent
        layer="below",  # Ensure the shape is below the data lines
        line_width=0,
    )
    # Add an annotation for the first axis if needed to label it as 'Strategy Options'
    fig.add_annotation(
        x=0,  # Position at the start
        y=.85,  # Slightly above the plot
        text="<b>Alternative Pathways</b>",  # Custom text
        showarrow=False,  # No arrow needed
        xref="paper",
        yref="paper",
        font=dict(size=12, color="black"),  # Make the font bold
        xanchor="left",
        yanchor="bottom",
    )

    # Add an annotation for the first axis if needed to label it as 'Objective performance'
    fig.add_annotation(
        x=.26 + (1. - 0.26) / 2,  # Position at the start
        y=.85,  # Slightly above the plot
        text="<b>Performance Criteria</b>",  # Custom text
        showarrow=False,  # No arrow needed
        xref="paper",
        yref="paper",
        font=dict(size=12, color="black"),  # Make the font bold
        xanchor="center",
        yanchor="bottom",
    )


    fig.update_layout(
        # Title and positioning
        title={'text': add_line_breaks(figure_title, 50), 'y': .95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom'},

        # Update layout to show the legend
        legend=dict(
            title='Legend',
            itemsizing='constant'
        ),
        title_font_size=18,
        font_size=14,

        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        xaxis2=dict(visible=False),
        yaxis2=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',  # Make the plot background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot area background transparent

        # Custom margins
        # margin=dict(t=50, b=50),  # Final margin settings as it appears you've adjusted them
        margin=dict(l=5, r=5, t=30, b=5),
        # Fixed dimensions for the plot
        width=667,  # Width set to 1300 pixels
        height=567,  # Height set to 600 pixels
        autosize=False,  # Disable autosizing to use the specified width and height

    )
    return fig