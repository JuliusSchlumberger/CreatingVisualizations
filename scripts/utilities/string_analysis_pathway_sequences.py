import pandas as pd
import re

result_dict = {}

def process_string_old(s, result_dict, counter_dict):


    for match in re.finditer(r'(\d+)', s):
        num = int(match.group())
        # Get the index of the start of the number
        index = match.start()
        end_index = match.end()

        # Extract the substring before the number
        prefix = s[:index]

        # Extract the substring after the number
        suffix = s[end_index:]

        # check if next integer is end integer
        match_suffix = re.search(r'(\d+)', suffix)
        if match_suffix:
            first_integer_after = int(match_suffix.group(1))
        else:
            first_integer_after = 'No integers found in string'

        num_str = str(num)

        if num_str not in result_dict:
            result_dict[num_str] = {}
            counter_dict[num_str] = 0
            result_dict[num_str].update({prefix: f'{num_str}[{counter_dict[num_str]}]'})
        else:
            if prefix not in result_dict[num_str] and first_integer_after != 99:
                counter_dict[num_str] += 1
                result_dict[num_str].update({prefix: f'{num_str}[{counter_dict[num_str]}]'})
                search_fix = prefix

                # print(s, prefix, suffix, num_str, search_fix, f'{num_str}[{counter_dict[num_str]}]')
            # if prefix not in result_dict[num_str] and first_integer_after != 99:
            #     counter_dict[num_str] += 1
            #     result_dict[num_str].update({prefix: f'{num_str}[{counter_dict[num_str]}]'})
            #     search_fix = prefix
            #
            #     # print(s, prefix, suffix, num_str, search_fix, f'{num_str}[{counter_dict[num_str]}]')
            #
            # elif prefix not in result_dict[num_str] and first_integer_after == 99:  # ensure that measure instance, that lasts till end has separate tipping point
            #     counter_dict[num_str] += 1
            #     search_fix = prefix + 'and_end'
            #     search_fix = prefix
            #     result_dict[num_str].update({search_fix: f'{num_str}[{counter_dict[num_str]}]'})
            #
            #     # print(s, prefix, suffix, num_str, search_fix, f'{num_str}[{counter_dict[num_str]}]')
            #
            elif first_integer_after == 99:  # ensure that measure instance, that lasts till end has separate tipping point
                counter_dict[num_str] += 1
                search_fix = prefix + 'and_end'
                # search_fix = prefix
                result_dict[num_str].update({search_fix: f'{num_str}[{counter_dict[num_str]}]'})
            else:
                continue
            print(s, prefix, suffix, num_str,search_fix, f'{num_str}[{counter_dict[num_str]}]')



def process_string(s, result_dict, counter_dict):
    # Step 1: Count the & characters
    ampersand_count = s.count('&')
    parts = s.split('&')

    # Find integer in the string
    for no_pathway_change in range(1, ampersand_count):

        num = parts[no_pathway_change]

        if num == '':
            continue
        else:
            prefix = '&'.join(str(number) for number in parts[:no_pathway_change]) + '&'

            # Extract the substring before the number
            if parts[no_pathway_change+1] == '99':
                search_fix = prefix + '99'
            else:
                search_fix = prefix
            # Measure number is not yet listed in dictionary
            if num not in result_dict:
                result_dict[num] = {}
                counter_dict[num] = 0
                result_dict[num].update({search_fix: f'{num}[{counter_dict[num]}]'})
            else: # Measure is already listed but specific pre-sequence is not there yet...
                # ... and the measure looked at is not the last one,
                if search_fix not in result_dict[num] and parts[no_pathway_change+1] != '99':
                    counter_dict[num] += 1
                    result_dict[num].update({search_fix: f'{num}[{counter_dict[num]}]'})
                # ... and the measure looked at is the last one,
                elif search_fix not in result_dict[num] and parts[no_pathway_change+1] == '99':
                    counter_dict[num] += 1
                    result_dict[num].update({search_fix: f'{num}[{counter_dict[num]}]'})

            # print(s, prefix, num, f'{num}[{counter_dict[num]}]')
