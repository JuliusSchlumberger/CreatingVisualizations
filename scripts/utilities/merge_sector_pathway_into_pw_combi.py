

def merge_sector_pathway_into_pw_combi(df, sh, rohs):
    # Find the position of the string
    pathways = df[sh]
    position = rohs.index(sh)
    default_pw_combi = [['00', '00', '00', '00']] * len(pathways)
    default_pw_combi[position] = pathways
    new_columns = '_'.join(default_pw_combi)
    print(default_pw_combi)
    print(default_pw_combi,'_'.join(default_pw_combi) )
    return '_'.join(default_pw_combi)