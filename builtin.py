import os
import vars
from myErrors import *

def handle(args):
    program = args[0]
    args = args[1:]
    match program:
        case "exit":
            exit(args)
        case "var":
            var(args)
        case "pwd":
            pwd(args)
        case "cd":
            cd(args)
        case _:
            return False
    return True



def var(args):
    pass 

def exit(args):
    os._exit(0)

def pwd(args):
    print(vars.get("cwd"))

def cd(args):
    if len(args) == 0:
        vars.set("cwd", os.path.expanduser("~"))
        return

    if len(args) > 1:
        raise errorMsg("cd: too many arguments\n")

    path = args[0]
    cwd = vars.get("cwd")
    # sets path initially as if it is a relative path, then if not it is overwritten
    new_path = os.path.join(cwd, path)

    # errors
    if not os.path.exists(new_path):
        raise errorMsg(f"cd: No such file or directory: {path}")
    if not os.path.isdir(new_path):
        raise errorMsg(f"cd: Not a directory: {path}")
    if not os.access(new_path, os.X_OK):
        raise errorMsg(f"cd: Permission denied: {path}")

    if path.startswith("/"):
        new_path = path
    
    else:
        if path == ".":
            return

        elif path == "..":
            if cwd == "/":
                return
            else:
                new_path = get_parent_path(cwd)
        
        elif os.path.islink(new_path):
            pass



    vars.set("cwd", new_path)

def get_parent_path(path):
    index = -1
    for i in range(len(path)):
        if path[i] == "/":
            index = i

    parent = ""
    for i in range(index):
        parent += path[i]

    return parent
