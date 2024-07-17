
def find_substring(target, string_list):
    for s in string_list:
        if s in target:
            return s
    return None