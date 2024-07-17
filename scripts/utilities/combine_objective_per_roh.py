import pandas as pd
from Paper3_v1.scripts.utilities.map_system_parameters import SECTOR_OBJECTIVES


def combine_objective_per_roh(risk_owner_of_interest,list_of_files):
    results = []
    # print(list_of_files)
    for pw_combi in list_of_files:
        df = pd.read_csv(pw_combi)
        risk_owner_hazard_df = df.copy()
        risk_owner_hazard_df = risk_owner_hazard_df[
            risk_owner_hazard_df.objective_parameter.isin(SECTOR_OBJECTIVES[risk_owner_of_interest])]
        results.append(risk_owner_hazard_df)

    return pd.concat(results, ignore_index=True)