"""
Module to run builtin commands, check if command is a builtin with
'is_builtin()' and run with 'handle()'
"""

import os
import settings
from my_errors import ErrorMsg
import parsing
import command

builtins = [
        "exit",
        "var",
        "pwd",
        "cd",
        "which",
        ]

def is_builtin(program):
    """
    Returns True if a program is a builtin and false otherwise
    """
    return program in builtins

def handle(args):
    """
    Function to run a builtin program
    Program name should be first argument
    """
    program = args[0]
    args = args[1:]
    match program:
        case "exit":
            return exit_func(args)
        case "var":
            return var(args)
        case "pwd":
            return pwd(args)
        case "cd":
            return cd(args)
        case "which":
            return which(args)

def which(args):
    """
    Runs the 'which' builtin, program name should not be included in args
    """
    if len(args) == 0:
        raise ErrorMsg("usage: which command ...")
    res = ""
    for arg in args:
        if arg in builtins:
            res += f"{arg}: shell built-in command\n"
            continue

        if (path := search_path_for_executable(arg)) is not None:
            if os.access(path, os.X_OK):
                res += f"{path}\n"
            else:
                res += f"mysh: permission denied: {path}"
        else:
            res += f"{arg} not found\n"

    return res.rstrip()

def search_path_for_executable(program):
    """
    Searches the path for an executable, returns None if not found
    """
    locs = settings.get_var("PATH").split(os.pathsep)
    for loc in locs:
        exec_path = os.path.join(loc, program)
        if os.path.isfile(exec_path):
            return exec_path
    return None


def exit_func(args):
    """
    Runs the 'exit' builtin, program name should not be included in args
    Inconsistent naming to avoid overwriting python 'exit' function
    """
    if len(args) == 0:
        os._exit(0)

    if len(args) > 1:
        raise ErrorMsg("exit: too many arguments")

    if not args[0].isnumeric():
        raise ErrorMsg(f"exit: non-integer exit code provided: {args[0]}")

    os._exit(int(args[0]))

def var(args):
    """
    Runs the 'var' builtin, program name should not be included in args
    """
    if len(args) != 2 and len(args) != 3:
        raise ErrorMsg(f"var: expected 2 arguments, got {len(args)}")

    if len(args) == 3:
        if args[0] == "-s":
            new_args = parsing.get_tokens(args[2])
            res = command.run_command(new_args, True)

            # removed return not sure if can be deleted
            # look in mysh loop some reason this is needed
            # if is_executable:
            #     res = res.rstrip()

            settings.set_var(args[1], res)
            return

        if args[0].startswith("-"):
            raise ErrorMsg(f"var: invalid option: {args[0][:2]}")

        # first arg is not a flag
        raise ErrorMsg(f"var: expected 2 arguments, got {len(args)}")

    if len(args) == 2:
        if not args[0].replace("_", "").isalnum():
            raise ErrorMsg(f"var: invalid characters for variable {args[0]}")

    settings.set_var(args[0], args[1])


def pwd(args):
    """
    Runs the 'pwd' builtin, program name should not be included in args
    """
    if len(args) == 0:
        return settings.get_var("PWD")

    if len(args) == 1 and args[0] == "-P":
        path = os.path.realpath(settings.get_var("PWD"))
        return path

    if args[0].startswith("-"):
        raise ErrorMsg(f"pwd: invalid option: {args[0][:2]}")

    raise ErrorMsg("pwd: not expecting any arguments")

def cd(args):
    """
    Runs the 'cd' builtin, program name should not be included in args
    """
    if len(args) == 0:
        settings.set_var("PWD", os.path.expanduser("~"))
        return

    if len(args) > 1:
        raise ErrorMsg("cd: too many arguments")

    path = args[0]
    cwd = settings.get_var("PWD")
    # sets path initially as if it is a relative path, then if not it is overwritten
    new_path = os.path.join(cwd, path)

    # handled in run_command()
    # if path == "~":
    #     new_path = os.path.expanduser("~")

    # errors
    if not os.path.exists(new_path):
        raise ErrorMsg(f"cd: no such file or directory: {path}")
    if not os.path.isdir(new_path):
        raise ErrorMsg(f"cd: not a directory: {path}")
    if not os.access(new_path, os.X_OK):
        raise ErrorMsg(f"cd: permission denied: {path}")

    if path.startswith("/"):
        new_path = path

    else:
        if path == ".":
            return

        if path == "..":
            if cwd == "/":
                return

            new_path = get_parent_path(cwd)

    settings.set_var("PWD", new_path)

def get_parent_path(path):
    """
    Returns the parent path of a provided path
    """
    index = -1
    for i, char in enumerate(path):
        if char == "/":
            index = i

    parent = ""
    for i in range(index):
        parent += path[i]

    return parent
