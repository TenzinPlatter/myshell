"""
Module containing global env variables
"""

import os
from config import parse_config_file
import my_vars

def init():
    """
    Sets initial variables, should only be called ONCE
    """
    my_vars.init()

    if not (prompt := my_vars.get_var("PROMPT")):
        prompt = ">> "
    path = my_vars.get_var("PATH")

    if not my_vars.var_exists("MYSHDOTDIR"):
        my_vars.set_var("MYSHDOTDIR", os.path.expanduser("~"))

    config_path = os.path.join(my_vars.get_var("MYSHDOTDIR"), ".myshrc")

    my_vars.set_var("PATH", path)
    my_vars.set_var("PROMPT", prompt)
    my_vars.set_var("PWD", os.getcwd())
    my_vars.set_var("MYSH_VERSION", "1.0")
    parse_config_file(config_path)
