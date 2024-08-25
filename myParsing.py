import settings
import shlex

def filter_vars(data):
    indexes = get_var_indexes(data)
    for index_pair in indexes:
        var_name = data[index_pair[0] + 2 : index_pair[1]]
        var_val = settings.get_var(var_name)
        data = replace_substr(data, var_val, index_pair[0], index_pair[1])
    return data

def replace_substr(string, substr, start, end):
    """replaces the string between start and end indexes with substr
    start and end are inclusive for substr position"""
    result = ""
    added = False
    for i in range(len(string)):
        if i < start or i > end:
            result += string[i]
        elif not added:
            result += substr
            added = True
    return result

def get_var_indexes(data):
    indexes = []
    curr_index = []
    last_was_start = False
    escaped = False
    in_var = False
    for i in range(len(data)):
        chr = data[i]

        if chr == "\\" and not in_var:
            escaped = True
            continue

        if not in_var and not last_was_start and not escaped and chr == "$":
            last_was_start = True
            continue

        if last_was_start and chr == "{":
            in_var = True
            curr_index.append(i - 1)

        if in_var and chr == "}":
            in_var = False
            curr_index.append(i)
            indexes.append(curr_index)
            curr_index = []
            continue

        escaped = False
        last_was_start = False
    return indexes

def get_tokens_obj(data):
    data = filter_vars(data)
    tokens = shlex.shlex(data, posix = True)
    tokens.escapedquotes = "'\""
    tokens.wordchars += "-./${}"
    tokens.whitespace_split = True
    return tokens

def get_tokens_list(data):
    filtered_data = filter_vars(data)
    tokens_obj = get_tokens_obj(filtered_data)
    args = [token for token in tokens_obj]
    for i in range(len(args)):
        if "\\" in args[i]:
            args[i] = args[i].replace("\\", "")
    return args
