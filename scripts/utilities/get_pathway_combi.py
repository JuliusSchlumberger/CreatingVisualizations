

def get_pathway_combi(model_output):
    # Step 1: Split by '/' and take the last element
    filename = model_output.split('/')[-1]

    # Step 2: Split by '_' and take the substring right of the first '_',
    # which means joining the parts from the second element onwards
    substring_after_first_underscore = '_'.join(filename.split('_')[1:])

    # Step 3: Remove the last 7 characters
    return substring_after_first_underscore[:-7]