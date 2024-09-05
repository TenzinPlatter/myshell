"""
Contains 'get_config_vars' function to retrieve dictionary of all valid
variables set in .myshrc
"""
import json
import sys
from parsing import filter_vars
from my_errors import ErrorMsg
import settings

def parse_config_file(config_path) -> list | None:
    """
    - Call this to return a dictionary of all vars set in the myshrc
    - Checks for MYSHDOTDIR internally
    - Returns None if no config file found
    """
    var_pairs = []

    try:
        with open(config_path, "r", encoding = "utf-8") as config_file:
            # raises ErrorMsg if json invalid
            var_pairs = get_pairs(config_file)
    except ErrorMsg as e:
        sys.stderr.write(e.msg + "\n")
    except FileNotFoundError:
        return

    for key, val in var_pairs:
        # error cases
        if not key.replace("_", "").isalnum():
            sys.stderr.write(f"mysh: .myshrc: {key}: invalid characters for variable name\n")
            continue

        if not isinstance(val, str):
            sys.stderr.write(f"mysh: .myshrc: {key}: not a string\n")
            continue

        val = filter_vars(val)
        settings.set_var(key, val)

def get_pairs(file) -> list:
    """
    Parses a file as a string and returns each key value pair
    - Assumes no nested variables
    - Throws ErrorMsg if invalid syntax
    """
    data = file.read()
    try:
        return json.loads(
                data,
                object_pairs_hook = lambda pairs: [[key, value] for key, value in pairs]
                )
    except Exception as e:
        raise ErrorMsg("mysh: invalid JSON format for .myshrc") from e
