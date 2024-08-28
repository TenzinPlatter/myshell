import os

def init():
    global env_vars
    env_vars = dict(os.environ)

def set_var(name, val):
    """
    Sets an env variable
    """
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
