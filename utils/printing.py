def print_blank_spaces(length, word_length):
    for _ in range(length - word_length):
        print(" ", end="")

def print_item(item, columns, columns_lengths):
    for i, col in enumerate(columns):
        print(item.get(col), end="")
        print_blank_spaces(columns_lengths.get(col), len(str(item.get(col))))
        if i != len(columns) - 1:
            print("|", end="")
    print()

def print_header(columns, columns_aliases, columns_lengths):
    print_item(columns_aliases, columns, columns_lengths)

def print_item_list(item_list, columns, columns_aliases, columns_lengths):
    print_header(columns, columns_aliases, columns_lengths)
    for item in item_list:
        print_item(item, columns, columns_lengths)

def get_max_columns_lengths(item_list, columns, columns_aliases):
    lengths = {}
    for col in columns:
        lengths[col] = len(columns_aliases.get(col))
    for item in item_list:
        for col in columns:
            lengths[col] = max(lengths[col], len(str(item.get(col))))
    return lengths
