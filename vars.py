import os

def init():
    global vars
    vars = {}

    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">>"

    if not (path := os.environ.get("PATH")):
        path = os.defpath

    set("path", path)
    set("prompt", prompt)
    set("cwd", os.getcwd())

def set(name, val):
    vars[name] = val

def get(name):
    if name not in vars.keys():
        return None

    return vars[name]
