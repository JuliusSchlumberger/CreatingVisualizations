

# extra functions
def insert_linebreak(s, max_length=20):
    if len(s) <= max_length:
        return s

    # Find the nearest space before or at max_length
    break_point = max_length
    while s[break_point] != ' ' and break_point > 0:
        break_point -= 1

    if break_point == 0:
        return s  # No space found; return the original string

    # Insert line break
    return s[:break_point] + '\n' + s[break_point + 1:]