
def find_key_by_value_string(my_dict, search_str):
    for key, value in my_dict.items():
        if search_str in value:
            return key
    return None  # If the string is not found in any value
