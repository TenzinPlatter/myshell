from myErrors import errorMsg
import signal
import os
import builtin
import settings

# duped to prevent a future import loop
def search_path_for_executable(program):
    locs = settings.get_var("path").split(os.pathsep)
    for loc in locs:
        exec_path = os.path.join(loc, program)
        if os.path.isfile(exec_path):
            return exec_path
    return None

def run_command(args):
    program = args[0]

    # returns true if program is a builtin else false and continues
    if builtin.is_builtin(program):
        return builtin.handle(args)

    if (path := search_path_for_executable(program)) == None:
        print(path)
        raise errorMsg(f"mysh: no such file or directory: {program}")
    else:
        args[0] = path
        if os.access(path, os.X_OK):
            run_executable(args)
            return
        else:
            raise errorMsg(f"mysh: permission denied: {path}")

    if "/" in program:

        if os.path.isdir(program):
            raise errorMsg(f"mysh: is a directory: {program}")

        # checks if user has execute permissions
        if not os.access(program, os.X_OK):
            raise errorMsg(f"mysh: permission denied: {program}")

        run_executable(args)
        return None

    raise errorMsg(f"mysh: command not found: {program}")

def handle_child_process(child_pid):
    #INFO: Unused, something about this in the specifications, but can't get
    # <C-c> to print new line when used on a child process when adjusting
    # permissions with this
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
    #TODO: fix keyboard interrupt not printing new line for subprocess
    child_pid = os.fork()

    if child_pid > 0:
        handle_child_process(child_pid)
        return

    elif child_pid == 0:
        os.setpgid(0, 0)
        program = args[0]
        os.execv(program, args)

