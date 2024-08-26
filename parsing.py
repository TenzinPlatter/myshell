"""
Module to handle parsing for the shell.
"""
import re
import shlex
import settings
from my_errors import ErrorMsg

def filter_vars(data) -> str:
    """
    Filters out variables defined by ${<name>} syntax, and replaces them with their
    value
    Returns new string
    """
    indexes = get_var_indexes(data)
    for index_pair in indexes:
        var_name = data[index_pair[0] + 2 : index_pair[1]]

        if not var_name.replace("_", "").isalnum():
            raise ErrorMsg(f"mysh: syntax error: invalid characters for variable {var_name}")

        if settings.var_exists(var_name):
            var_val = settings.get_var(var_name)
        else:
            var_val = ""
        data = replace_substr(data, var_val, index_pair[0], index_pair[1])
    return data

def replace_substr(string, substr, start, end):
    """
    replaces the string between start and end indexes with substr
    start and end are inclusive for substr position
    """
    result = ""
    added = False
    for i, char in enumerate(string):
        if i < start or i > end:
            result += char
        elif not added:
            result += substr
            added = True
    return result

def get_var_indexes(data):
    """
    Returns a list of tuples of index pairs for the start and ends of variables
    in the passed in string
    """
    indexes = []
    curr_index = []
    last_was_start = False
    escaped = False
    in_var = False
    for i, char in enumerate(data):
        if char == "\\" and not in_var:
            escaped = True
            continue

        if not in_var and not last_was_start and not escaped and char == "$":
            last_was_start = True
            continue

        if last_was_start and char == "{":
            in_var = True
            curr_index.append(i - 1)

        if in_var and char == "}":
            in_var = False
            curr_index.append(i)
            indexes.append(curr_index)
            curr_index = []
            continue

        escaped = False
        last_was_start = False
    return indexes

def get_tokens_obj(data):
    """
    Gets a shlex object of tokens
    """
    data = filter_vars(data)
    tokens = shlex.shlex(data, posix = True)
    tokens.escapedquotes = "'\""
    tokens.wordchars += "-./${}"
    tokens.whitespace_split = True
    return tokens

def get_tokens(data):
    """
    Returns fully processed tokens from input string
    """
    filtered_data = filter_vars(data)
    tokens_obj = get_tokens_obj(filtered_data)
    args = list(tokens_obj)
    for i, _ in enumerate(args):
        if "\\" in args[i]:
            args[i] = args[i].replace("\\", "")
    return args

_PIPE_REGEX_PATTERN = re.compile(
    # Match escaped double quotes
    r"\\\""
    # OR match escaped single quotes
    r"|\\'"
    # OR match strings in double quotes (escaped double quotes inside other quotes are OK)
    r"|\"(?:\\\"|[^\"])*\""
    # OR match strings in single quotes (escaped single quotes inside other quotes are OK)
    r"|'(?:\\'|[^'])*'"
    # OTHERWISE: match the pipe operator, and make a capture group for this
    r"|(\|)"
)
"""
Regex pattern which will perform multiple matches for escaped quotes or quoted strings,
but only contain a capture group for an unquoted pipe operator ('|').

Original regex credit to zx81 on Stack Overflow (https://stackoverflow.com/a/23667311).
"""


def split_by_pipe_op(cmd_str: str) -> list[str]:
    """
    Split a string by an unquoted pipe operator ('|').

    The logic for this function was derived from 
    https://www.rexegg.com/regex-best-trick.php#notarzan.

    >>> split_by_pipe_op("a | b")
    ['a ', ' b']
    >>> split_by_pipe_op("a | b|c")
    ['a ', ' b', 'c']
    >>> split_by_pipe_op("'a | b'")
    ["'a | b'"]
    >>> split_by_pipe_op("a '|' b")
    ["a '|' b"]
    >>> split_by_pipe_op(r"a | b 'c|d'| ef\\"|\\" g")
    ['a ', " b 'c|d'", ' ef\\\\"', '\\\\" g']
    >>> split_by_pipe_op("a|b '| c' | ")
    ['a', "b '| c' ", ' ']

    Args:
        cmd_str: The command string we wish to split on the unquoted pipe operator ('|').

    Returns:
        A list of strings that was split on the unquoted pipe operator.
    """
    # If you'd like, you're free to modify this function as you need.

    # Indexes which we will split the string by
    split_str_indexes = []

    for match in _PIPE_REGEX_PATTERN.finditer(cmd_str):
        if match.group(1) is not None:
            # A group exists - which is only for the last alternative
            # All other alternatives have non-capture groups, meaning they will have
            # `group(1)` return `None`
            split_str_indexes.append(match.start())

    if not split_str_indexes:
        # Nothing to split
        return [cmd_str]

    # Now, we actually split the string by the pipe operator (identified at indexes in
    # `split_str_indexes`)
    split_str = []
    prev_index = 0
    for next_index in split_str_indexes:
        # Slice string
        cmd_str_slice = cmd_str[prev_index:next_index]
        split_str.append(cmd_str_slice)

        # Update index
        prev_index = next_index + 1

    cmd_str_slice = cmd_str[prev_index:]
    split_str.append(cmd_str_slice)

    # Return string list
    return split_str
