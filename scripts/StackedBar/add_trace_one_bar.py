import plotly.graph_objects as go  # Import Plotly's graph_objects module
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV
from scripts.design_choices.colors import SECTOR_OBJECTIVE_COLORS


def add_traces_oneBar(plot_objectives, sector_objectives, plot_df, text_df, text_df_benchmark, risk_owner_hazard, offsetgroup, legend_entries, groupname_base):
    group_entries = []
    traces = []
    # Iterate through each column

    # Dictionary to store the cumulative values for each group
    cumulative_values = {
        0: {'pos': {row: 0 for row in plot_df[risk_owner_hazard]},
            'neg': {row: 0 for row in plot_df[risk_owner_hazard]}},
        1: {'pos': {row: 0 for row in plot_df[risk_owner_hazard]},
            'neg': {row: 0 for row in plot_df[risk_owner_hazard]}},
        2: {'pos': {row: 0 for row in plot_df[risk_owner_hazard]},
            'neg': {row: 0 for row in plot_df[risk_owner_hazard]}}
        }

    for col in sorted(plot_objectives):
        # Iterate through each row to add individual traces
        for i in plot_df.index:
            if col in sector_objectives:
                old_column_name = f'{col}_old'
                reference_case = [f'(baseline: {int(text_df_benchmark.at[0, col])}) MEUR' if offsetgroup == 0 else
                                f'(no interaction: {int(text_df_benchmark.at[i, old_column_name])}) MEUR'][0]

                hover_text = (
                    f"<b>{ROH_DICT_INV[risk_owner_hazard]} pathway {i}</b><br>"
                    f"{col}: {int(text_df.at[i, col])} {reference_case}"
                )
                groupname = groupname_base
            elif col.endswith('tradeoff'):
                obj_key = [column for column in sector_objectives if col.startswith(column)][0]
                hover_text = (
                    f"<b>{ROH_DICT_INV[risk_owner_hazard]} pathway {i}</b><br>"
                    f"interaction trade-off increasing {obj_key} by<br>"
                    f"{int(text_df_benchmark.at[i, col])} MEUR"
                )
                groupname = 'show synergies and tradeoffs'
            else:  # '_synergy'
                obj_key = [column for column in sector_objectives if col.startswith(column)][0]
                hover_text = (
                    f"<b>{ROH_DICT_INV[risk_owner_hazard]} pathway {i}</b><br>"
                    f"interaction synergy reducing {obj_key} by<br>"
                    f"{int(text_df_benchmark.at[i, col])} MEUR"
                )
                groupname = 'show synergies and tradeoffs'

            # Define the base objective
            base_objective = [objective for objective in sector_objectives if col.startswith(objective)]
            color = SECTOR_OBJECTIVE_COLORS[risk_owner_hazard][base_objective[0]]
            pattern = dict(shape='/', bgcolor=color, fgcolor='white') if col.endswith('_tradeoff') else dict(shape='.',
                                                                                                             bgcolor=color,
                                                                                                             fgcolor='white') if col.endswith(
                '_synergy') else None

            # Calculate the base for stacking
            base = cumulative_values[offsetgroup]['pos'][i]
            cumulative_values[offsetgroup]['pos'][i] += plot_df.at[i, col]

            # Determine if this legend entry has already been added
            showlegend = False

            if col not in legend_entries:
                legend_entries[col] = [color, pattern]
            if groupname not in group_entries:
                group_entries.append(groupname)
                showlegend = True

            # Add individual trace for each row
            traces.append(go.Bar(
                name=groupname,
                x=[plot_df.at[i, col]],
                y=[str(plot_df.at[i, risk_owner_hazard])],
                offsetgroup=offsetgroup,
                orientation='h',
                # base=base,  # Set the base for stacking
                hovertemplate=hover_text,
                # hoverinfo='text',
                marker=dict(color=color, pattern=pattern),
                showlegend=showlegend,
                legendgroup=groupname  # Use legendgroup to separate legends
            ))
    return traces, legend_entries

