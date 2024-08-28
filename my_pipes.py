# stdin, stdout, stderr
# 0, 1, 2

import os
import signal
from my_errors import ErrorMsg

def run_commands_with_pipes(command_list):
    processes = []
    
    # Set up a signal handler to terminate all processes on Ctrl+C
    def signal_handler(*_):
        for process in processes:
            try:
                os.kill(process, signal.SIGTERM)
            except ProcessLookupError:
                pass
        raise ErrorMsg("")

    signal.signal(signal.SIGINT, signal_handler)
    
    # File descriptors for the previous process's output (initially None)
    last_r = None
    
    for command in command_list:
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

            os.execvp(command[0], command)

    if last_r:
        output = os.read(last_r, 4096)
        os.close(last_r)
        return output.decode()
