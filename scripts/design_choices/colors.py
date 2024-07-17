from scripts.map_system_parameters import SECTOR_OBJECTIVES
from scripts.design_choices.main_dashboard_design_choices import OBJECTIVE_COLORS

SECTOR_OBJECTIVE_COLORS = {}
for key in SECTOR_OBJECTIVES:
    SECTOR_OBJECTIVE_COLORS[key] = {objective: OBJECTIVE_COLORS[key][i] for i, objective in enumerate(SECTOR_OBJECTIVES[key])}