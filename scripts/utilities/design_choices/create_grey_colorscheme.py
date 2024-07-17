from dataclasses import dataclass
from typing import List, Tuple
from Paper3_v1.scripts.utilities.design_choices.get_collection_lengths import get_collection_lengths

Colour = Tuple[float, float, float, float]
Colours = List[Colour]


@dataclass
class PlotColours:
    node_colours: Colours | None = None
    edge_colours: Colours | None = None
    node_edge_colours: Colours | None = None
    label_colour: Colour | None = None


def create_grey_plot_colours(ax, grey_value: float, alpha: float = 1.0) -> PlotColours:
    """
    Create a PlotColours instance with all elements set to the same shade of grey.

    :param grey_value: A float from 0 to 1 representing the grey shade (0 is black, 1 is white).
    :param alpha: A float from 0 to 1 representing the opacity (1 is fully opaque).
    :return: A PlotColours instance with grey colours.
    """
    # Use this function to get the lengths for a specific Axes object
    node_colours_length, edge_colours_length = get_collection_lengths(ax)
    length_of_input = max(edge_colours_length, node_colours_length)

    grey_colour = (grey_value, grey_value, grey_value, alpha)  # Grey RGBA colour
    grey_colours = [grey_colour] * length_of_input  # Assuming each colour attribute can accept a list of colours

    return PlotColours(
        node_colours=grey_colours,
        edge_colours=grey_colours,
        node_edge_colours=grey_colours,
        label_colour=grey_colour
    )
