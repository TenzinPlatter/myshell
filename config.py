"""
Contains 'get_config_vars' function to retrieve dictionary of all valid
variables set in .myshrc
"""

import json
import sys
from parsing import filter_vars

#TODO: parse variables for variables
def get_config_vars(config_path) -> dict | None:
    """
    - Call this to return a dictionary of all vars set in the myshrc
    - Checks for MYSHDOTDIR internally
    - Returns None if no config file found
    """
    vars_dict = {}

    try:
        with open(config_path, "r", encoding = "utf-8") as config_file:
            vars_dict = json.load(config_file)
    except FileNotFoundError:
        return None
    except:
        sys.stderr.write("mysh: invalid JSON format for .myshrc\n")
        return None

    to_del_keys = []

    for key, val in vars_dict:
        # error cases
        if not isinstance(val, str):
            sys.stderr.write(f"mysh: .myshrc: {val} not a string\n")
            to_del_keys.append(key)
            continue

        vars_dict[key] = filter_vars(val)

        if not key.replace("_", "").isalnum():
            sys.stderr.write(f"mysh: .myshrc: {val}: not a string\n")
            to_del_keys.append(key)
            continue

    while (key := to_del_keys.pop()):
        del vars_dict[key]

    return vars_dict
