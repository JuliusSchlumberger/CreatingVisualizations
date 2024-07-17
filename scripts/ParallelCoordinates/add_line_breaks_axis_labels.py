

# Define a function to add line breaks to long titles
def add_line_breaks(title, max_length=15):
    lines = []
    while len(title) > max_length:
        break_pos = max_length
        while break_pos < len(title) and title[break_pos] not in [' ', '_']:
            break_pos += 1
        if break_pos == len(title):
            break_pos = len(title)
        lines.append(title[:break_pos])
        title = title[break_pos:].lstrip(' _')
    lines.append(title)
    return '<br>'.join(lines)