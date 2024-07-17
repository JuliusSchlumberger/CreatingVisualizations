

def get_relevant_dfs(risk_owner_hazard, interactions_of_interest, df_timehorizons_dict, roh_list):
    if interactions_of_interest is None:
        relevant_df_no_interaction = df_timehorizons_dict[risk_owner_hazard]
        relevant_df_interaction = relevant_df_no_interaction.copy()
    else:
        active_for_interactions = [risk_owner_hazard] + interactions_of_interest
        key = '_'.join(sorted(active_for_interactions))
        relevant_df_no_interaction = df_timehorizons_dict[risk_owner_hazard]
        relevant_df_interaction = df_timehorizons_dict[key]

    relevant_df_no_interaction[roh_list] = relevant_df_no_interaction.pw_combi.str.split('_', expand=True)
    relevant_df_interaction[roh_list] = relevant_df_interaction.pw_combi.str.split('_', expand=True)

    return relevant_df_no_interaction, relevant_df_interaction
