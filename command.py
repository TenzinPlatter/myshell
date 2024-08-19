from myErrors import errorMsg
import signal
import os

def run_command(args):
    program = args[0]
    builtins = {
            "exit":
            "var"
            }

    if program in builtins:
        #implement once builtins are implemented
        return

    if "/" in program:
        if not os.path.exists(program):
            raise errorMsg(f"mysh: no such file or directory: {program}\n")

        if os.path.isdir(program):
            raise errorMsg(f"mysh: is a directory: {program}\n")

        # checks if user has execute permissions
        if not os.access(program, os.X_OK):
            raise errorMsg(f"mysh: permission denied: {program}\n")

        run_executable(args)
        return

    raise errorMsg(f"mysh: program not found: {program}\n")

def handle_child_process(child_pid):
    def handle_interrupt():
        print("Hello")
        return
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
        signal.signal(signal.SIGINT, handle_interrupt)
        os.execv(program, args)

