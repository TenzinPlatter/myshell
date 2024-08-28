"""
Module to run a command using 'run_command' function to run either builtin
or executable, or run an executable directly with 'run_executable'
"""

import os
import builtin
import my_vars
from my_errors import ErrorMsg

def run_command(args):
    """
    Takes in tokens as 'args' from a command line input and runs command
    Always returns output
    Takes read and write for pipe for use when using pipes
    """
    program = args[0]
    # skip program arg
    for i in range(len(args) - 1):
        args[i + 1] = os.path.expanduser(args[i + 1])

    # returns true if program is a builtin else false and continues
    if builtin.is_builtin(program):
        return builtin.handle(args)

    if "/" in program:
        if os.path.isdir(program):
            raise ErrorMsg(f"mysh: is a directory: {program}")

        # checks if user has execute permissions
        if not os.access(program, os.X_OK):
            raise ErrorMsg(f"mysh: permission denied: {program}")

        return run_executable(args)

    if (path := search_path_for_executable(program)) is None:
        raise ErrorMsg(f"mysh: command not found: {program}")

    args[0] = path
    if os.access(path, os.X_OK):
        return run_executable(args)

    raise ErrorMsg(f"mysh: permission denied: {path}")

def search_path_for_executable(program):
    """
    Searches path for an executable, returns None if not found
    Duped to prevent an import loop with builtin
    """
    locs = my_vars.get_var("PATH").split(os.pathsep)
    for loc in locs:
        exec_path = os.path.join(loc, program)
        if os.path.isfile(exec_path):
            return exec_path
    return None

def handle_child_process(child_pid):
    """
    Handles changing child process into terminal foreground group as specified
    in specifications
    """

    # doesn't work for child process, and afterwards acts as interrupt for all
    # SIGINT's
    # signal.signal(signal.SIGINT, interrupt_handler)
    try:
        os.setpgid(child_pid, child_pid)
    except PermissionError:
        pass
    parent_pgid = os.getpgrp()
    child_pgid = os.getpgid(child_pid)
    file_descriptor = os.open("/dev/tty", os.O_RDONLY)
    os.tcsetpgrp(file_descriptor, child_pgid)
    os.wait()
    os.tcsetpgrp(file_descriptor, parent_pgid)
    os.close(file_descriptor)

def run_executable(args):
    """
    Runs an executable, path passed in should be absolute
    If return_output is True then will redirect stdout and return it else 
    will return None
    """
    #TODO: fix keyboard interrupt not printing new line for subprocess

    r, w = os.pipe()


    pid = os.fork()

    # parent process
    if pid > 0:
        handle_child_process(pid)

        # stdout redirect
        os.close(w)
        with os.fdopen(r) as pipe_read:
            output = pipe_read.read()

        # lil bit hacky but ???
        # remove newline added by echo
        # avoided strip to not remove extra whitespace
        if args[0].endswith("echo") and output[-1] == "\n":
            output = output[:-1]

        return output

    # child process
    else:
        os.close(r)
        os.dup2(w, 1)
        os.close(w)

        os.setpgid(0, 0)
        program = args[0]
        os.execv(program, args)
