import os
import settings
from myErrors import *

builtins = [
        "exit",
        "var",
        "pwd",
        "cd",
        "which",
        ]

def is_builtin(program):
    return program in builtins

def handle(args):
    program = args[0]
    args = args[1:]
    match program:
        case "exit":
            return exit(args)
        case "var":
            return var(args)
        case "pwd":
            return pwd(args)
        case "cd":
            return cd(args)
        case "which":
            return which(args)

def which(args):
    if len(args) == 0:
        raise errorMsg(f"usage: which command ...")
    res = ""
    for arg in args:
        if arg in builtins:
            res += f"{arg}: shell built-in command\n"
            continue
        
        if (path := search_path_for_executable(arg)) != None:
            if os.access(path, os.X_OK):
                res += f"{path}\n"
            else:
                res += f"mysh: permission denied: {path}"

        else:
            res += f"{arg} not found\n"

    return res.strip()

def search_path_for_executable(program):
    locs = settings.get_var("path").split(os.pathsep)
    for loc in locs:
        exec_path = os.path.join(loc, program)
        if os.path.isfile(exec_path):
            return exec_path
    return None


def exit(args):
    if len(args) == 0:
        os._exit(0)

    if len(args) > 1:
        raise errorMsg("exit: too many arguments")

    if not args[0].isnumeric():
        raise errorMsg(f"exit: non-integer exit code provided: {args[0]}")

    os._exit(int(args[0]))

def var(args):
    if len(args) != 2 and len(args) != 3:
        raise errorMsg(f"var: expected 2 arguments, got {len(args)}")


    if len(args) == 3:
        if args[0] == "-P":
            #TODO:
            return
        if args[0].startswith("-"):
            raise errorMsg(f"var: invalid option: {args[0][:2]}")

        # first arg is not a flag
        raise errorMsg(f"var: expected 2 arguments, got {len(args)}")

    if len(args) == 2:
        if not args[0].isalnum():
            raise errorMsg(f"var: invalid characters for variable {args[0]}")
    settings.set_var(args[0], args[1])


def pwd(args):
    if len(args) == 0:
        return settings.get_var("cwd")

    if len(args) == 1 and args[0] == "-P":
        path = os.path.realpath(settings.get_var("cwd"))
        return path

    if args[0].startswith("-"):
        raise errorMsg(f"pwd: invalid option: {args[0][:2]}")
    else:
        raise errorMsg(f"pwd: not expecting any arguments")
         

def cd(args):
    if len(args) == 0:
        settings.set_var("cwd", os.path.expanduser("~"))
        return

    if len(args) > 1:
        raise errorMsg("cd: too many arguments")

    path = args[0]
    cwd = settings.get_var("cwd")
    # sets path initially as if it is a relative path, then if not it is overwritten
    new_path = os.path.join(cwd, path)

    if path == "~":
        new_path = os.path.expanduser("~")

    # errors
    if not os.path.exists(new_path):
        raise errorMsg(f"cd: no such file or directory: {path}")
    if not os.path.isdir(new_path):
        raise errorMsg(f"cd: not a directory: {path}")
    if not os.access(new_path, os.X_OK):
        raise errorMsg(f"cd: permission denied: {path}")

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

    settings.set_var("cwd", new_path)

def get_parent_path(path):
    index = -1
    for i in range(len(path)):
        if path[i] == "/":
            index = i

    parent = ""
    for i in range(index):
        parent += path[i]

    return parent
