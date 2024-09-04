"""
Module containing global env variables
"""

import os
from config import parse_config_file

def init():
    """
    Sets initial variables, should only be called ONCE
    """
    global env_vars
    env_vars = os.environ

    prompt = get_var("PROMPT") if var_exists("PROMPT") else ">> "

    path = get_var("PATH") if var_exists("PATH") else os.defpath

    version = get_var("MYSH_VERSION") if var_exists("MYSH_VERSION") else "1.0"

    if not var_exists("MYSHDOTDIR"):
        set_var("MYSHDOTDIR", os.path.expanduser("~"))


    myshdotdir = get_var("MYSHDOTDIR")
    myshdotdir = os.path.expanduser(myshdotdir)

    config_path = os.path.join(myshdotdir, ".myshrc")

    set_var("PATH", path)
    set_var("PROMPT", prompt)
    set_var("PWD", os.getcwd())
    set_var("MYSH_VERSION", version)
    parse_config_file(config_path)

def set_var(name, val):
    """
    Sets an env variable
    """
    if name == "PWD":
        os.chdir(val)

    env_vars[name] = val

def get_var(name):
    """
    Returns an env variable
    """
    if name in env_vars:
        return env_vars[name]
    else:
        return ""

def var_exists(name):
    """
    Returns whether a variable with a given name exists, should be used to check
    before get_var
    """
    return name in env_vars

def get_env():
    return env_vars
