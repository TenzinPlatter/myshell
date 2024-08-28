import os

def init():
    global vars
    vars = dict(os.environ)

def set_var(name, val):
    """
    Sets an env variable
    """
    vars[name] = val

def get_var(name):
    """
    Returns an env variable
    """
    if name in vars:
        return vars[name]
    else:
        return ""

def var_exists(name):
    """
    Returns whether a variable with a given name exists, should be used to check
    before get_var
    """
    return name in vars
