"""
Module containing global env variables
"""

import os
from config import get_config_vars

def init():
    """
    Sets initial variables, should only be called ONCE
    """
    if not (prompt := get_var("PROMPT")):
        prompt = ">> "

    path = get_var("PATH")

    set_var("PATH", path)
    set_var("PROMPT", prompt)
    set_var("PWD", os.getcwd())
    set_var("MYSH_VERSION", "1.0")

    if "MYSHDOTDIR" not in os.environ:
        set_var("MYSHDOTDIR", os.path.expanduser("~"))

def set_config_vars():
    vars_dict = get_config_vars(f"{get_var("MYSHDOTDIR")}/.myshrc")

    if vars_dict is None:
        return

    for key, val in vars_dict:
        set_var(key, val)

def set_var(name, val):
    """
    Sets an env variable
    """
    os.environ[name] = val

def get_var(name):
    """
    Returns an env variable
    """
    if name not in os.environ:
        return ""

    return os.environ.get(name)

def var_exists(name):
    """
    Returns whether a variable with a given name exists, should be used to check
    before get_var
    """
    return name in os.environ
