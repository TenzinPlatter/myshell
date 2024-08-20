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
    if len(args) == 0:
        print(vars.get("cwd"))
        return

    if len(args) == 1 and args[0] == "-P":
        path = os.path.realpath(vars.get("cwd"))
        print(path)
        return

    if args[0].startswith("-"):
        raise errorMsg(f"pwd: invalid option: {args[0][:2]}\n")
    else:
        raise errorMsg(f"pwd: not expecting any arguments\n")
         


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

    if path == "~":
        new_path = os.path.expanduser("~")

    # errors
    if not os.path.exists(new_path):
        raise errorMsg(f"cd: no such file or directory: {path}\n")
    if not os.path.isdir(new_path):
        raise errorMsg(f"cd: not a directory: {path}\n")
    if not os.access(new_path, os.X_OK):
        raise errorMsg(f"cd: permission denied: {path}\n")

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
        

        # don't think this is needed
        # elif os.path.islink(new_path):
        #     new_path = os.path.realpath(new_path)

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
