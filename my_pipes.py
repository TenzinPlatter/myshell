"""
Module to handle input running commands with pipes
"""

import os
import signal
from my_errors import ErrorMsg
import parsing

def check_for_syntax_errors(command_list):
    """
    Checks the list of arguments for a pipe related syntax error
    """
    last_is_pipe = False

    for args in command_list:
        for arg in args:
            # two pipes with nothing inbetween
            if arg == "|":
                if last_is_pipe:
                    raise ErrorMsg("mysh: syntax error: expected command after pipe")

                last_is_pipe = True
            else:
                last_is_pipe = False

    # trailing pipe
    if last_is_pipe:
        raise ErrorMsg("mysh: syntax error: expected command after pipe")

def handle(command_list):
    """
    Closes all open processes on interrupt signal in order to fully exit pipe
    """
    processes = []

    def signal_handler(*_):
        for process in processes:
            try:
                os.kill(process, signal.SIGINT)
            except ProcessLookupError:
                pass

    signal.signal(signal.SIGINT, signal_handler)


    command_list = parsing.split_commands_by_pipe(command_list)
    check_for_syntax_errors(command_list)

    # file descriptors for the previous process's output (initially None)
    last_r = None

    for args in command_list:
        r, w = os.pipe()

        pid = os.fork()

        # parent process
        if pid:
            processes.append(pid)

            if last_r:
                os.close(last_r)
            if w:
                os.close(w)
            last_r = r
            os.wait()

        # child process
        else:
            if last_r:
                os.dup2(last_r, 0)
                os.close(last_r)
            if w:
                os.dup2(w, 1)
                os.close(w)

            os.execvp(args[0], args)

    if last_r:
        output = os.read(last_r, 4096)
        os.close(last_r)
        return output.decode()

    # unreachable
    return None
