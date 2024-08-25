import os

def init():
    global vars
    vars = {}

    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">>"

    if not (path := os.environ.get("PATH")):
        path = os.defpath

    set_var("path", path)
    set_var("prompt", prompt)
    set_var("cwd", os.getcwd())

def set_var(name, val):
    vars[name] = val

def get_var(name):
    if name not in vars.keys():
        return ""

    return vars[name]
