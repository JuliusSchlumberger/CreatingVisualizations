from Paper3_v1.scripts.utilities.map_system_parameters import MEASURE_DICT
from Paper3_v1.scripts.utilities.insert_linebreaks import insert_linebreak
from plotly.subplots import make_subplots

# Constants for legend layout
start_x = 0.07  # Starting x position for the first item
start_y = 0.08  # y position for logos and text, negative to place below the plot
x_increment = 0.15  # Increment x position for each subsequent item
y_increment = 0.1


def add_logos_legend(fig, legend_items):
    nr_rows = 0
    for i, item in enumerate(legend_items):
        # Calculate x position for the current item
        current_x = start_x + i * x_increment

        if current_x > 0.85:
            nr_rows += 1
            current_x -= i * x_increment
        else:
            nr_rows = nr_rows

        current_y = start_y - nr_rows * y_increment

        # Add logo image as layout image
        fig.add_layout_image(
            dict(
                source=item['logo'],
                xref="paper",
                yref="paper",
                x=current_x,
                y=current_y,
                sizex=0.05,  # Adjust size as needed
                sizey=0.05,  # Adjust size as needed
                xanchor="center",
                yanchor="middle"
            ),
        )

        # Add measure name as annotation (text)
        text = insert_linebreak((f"{MEASURE_DICT[item['name']]}"))
        # print(text)

        fig.add_annotation(
            x=current_x + 0.01,
            y=current_y,  # Adjust as needed to place text below the logo
            xref="paper",
            yref="paper",
            text=insert_linebreak((f"{MEASURE_DICT[item['name']]}")),
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            align="left",
        )

        # Calculate the box dimensions
    box_start_x = 0  # Slightly to the left of the first legend item for padding
    box_start_y = start_y + 0.05  # Slightly above the first row for padding
    box_end_x = 1  # Adjust based on your column count and padding
    box_end_y = start_y - (nr_rows * y_increment) - 0.05  # Extend below the last row with padding

    # Add "Legend" text at the top left corner of the box
    fig.add_annotation(
        x=box_start_x,
        y=box_start_y + 0.5 * (box_end_y - box_start_y),
        xref="paper",
        yref="paper",
        text="Legend",
        showarrow=False,
        xanchor="left",
        yanchor="middle",
        font=dict(
            size=14,
            color="black"
        ),
        align="left",
    )

    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=box_start_x,
        y0=box_start_y,
        x1=box_end_x,
        y1=box_end_y,
        line=dict(
            color="Black",
            width=1,
        ),
        # fillcolor="LightSkyBlue",  # Optional: fill color for the legend box, choose as per your design
    )

    return fig
