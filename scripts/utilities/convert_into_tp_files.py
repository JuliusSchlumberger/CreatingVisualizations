import pandas as pd
import re

def convert_into_tp_files_old(subset, mapping_dict):
    output_dict = {
        'conditional_measure': [],
        'tipping_point': []
    }
    conditional_measure = []
    tipping_point = []

    for index, row in subset.iterrows():
        tp_value = row['year'] + 2030
        sequence = row['Value']
        if sequence == '0&99':
            continue
        else:
            measure_integers = re.findall(r'\d+', sequence)
            # print(measure_integers)
            if len(measure_integers) <= 1:
                continue
            else:
                for match in re.finditer(r'(\d+)', sequence):
                    # print(match, measure_integers)
                    num = int(match.group())
                    if num == int(measure_integers[-2]):
                        # Get the index of the start of the number
                        index = match.start()
                        end_index = match.end()

                        # Extract the substring before the number
                        prefix = sequence[:index]

                        # Extract the substring after the number
                        suffix = sequence[end_index:]

                        # check if next integer is end integer
                        first_integer_after = int(re.search(r'(\d+)', suffix).group(1))

                        if str(num) == '0':
                            identifier_measure = 'current'
                        else:
                            # identifier = '&'.join(str(num) for num in parts[:ampersand_count-1]) + '&'
                            # print(ampersand_count, sequence, measure_to_find_allocate_tp, identifier, mapping_dict[measure_to_find_allocate_tp])

                            if first_integer_after == 99:
                                search_fix = prefix + 'and_end'
                                search_fix = prefix
                            else:
                                search_fix = prefix
                            print(measure_integers, num, search_fix)
                            identifier_measure = mapping_dict[str(num)][search_fix]
                            # print(sequence, num, tp_value, prefix, identifier_measure)
                            # print(measure_integers, num, search_fix, mapping_dict[str(num)][search_fix], int(tp_value))
                        conditional_measure.append(identifier_measure)
                        tipping_point.append(int(tp_value))

        output_dict['conditional_measure'] = conditional_measure
        output_dict['tipping_point'] = tipping_point

    df_output = pd.DataFrame(output_dict)
    df_output = df_output.drop_duplicates()

    return df_output


def convert_into_tp_files(subset, mapping_dict):
    output_dict = {
        'conditional_measure': [],
        'tipping_point': []
    }
    conditional_measure = []
    tipping_point = []

    for index, row in subset.iterrows():
        # print(row)
        tp_value = row['year'] + 2020
        sequence = row['implementation_across_multi_risk']
        parts = sequence.split('&')

        # Step 1: Count the & characters
        ampersand_count = sequence.count('&')

        measure_to_find_allocate_tp = parts[ampersand_count]

        if measure_to_find_allocate_tp == '0':
            identifier_measure = 'current'
        else:
            end_value = row['Value'].split('&')[-1]
            if end_value == '99':
                identifier = '&'.join(str(num) for num in parts[:ampersand_count]) + '&99'
            else:
                identifier = '&'.join(str(num) for num in parts[:ampersand_count]) + '&'

            print(ampersand_count, sequence, measure_to_find_allocate_tp, identifier, mapping_dict[measure_to_find_allocate_tp])
            identifier_measure = mapping_dict[measure_to_find_allocate_tp][identifier]
            print(identifier_measure)
        conditional_measure.append(identifier_measure)
        tipping_point.append(int(tp_value))
    output_dict['conditional_measure'] = conditional_measure
    output_dict['tipping_point'] = tipping_point

    df_output = pd.DataFrame(output_dict)
    df_output = df_output.drop_duplicates()

    return df_output