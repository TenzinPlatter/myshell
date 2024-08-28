# stdin, stdout, stderr
# 0, 1, 2

import os
import signal
import builtin
import settings

settings.init()

def run_commands_with_pipes(command_list):
    processes = []
    
    # Set up a signal handler to terminate all processes on Ctrl+C
    def signal_handler(*_):
        for process in processes:
            try:
                os.kill(process, signal.SIGTERM)
            except ProcessLookupError:
                pass
        raise Exception

    signal.signal(signal.SIGINT, signal_handler)
    
    # File descriptors for the previous process's output (initially None)
    last_out = None

    for args in command_list:
        # builtin
        if builtin.is_builtin(args[0]):
            last_out = builtin.handle(args)
            continue

        # else
        if last_out:
            stdin_pipe = os.pipe()
            os.write(stdin_pipe[1], last_out.encode())
            os.close(stdin_pipe[1])
            stdin = stdin_pipe[0]
        else:
            stdin = None

        stdout_pipe = os.pipe()
        pid = os.fork()

        # child
        if pid == 0:
            if stdin:
                os.dup2(stdin, 0)
                os.close(stdin)
            os.dup2(stdout_pipe[1], 1)
            os.close(stdout_pipe[1])
            os.close(stdout_pipe[0])

            os.execvp(args[0], args)

        # parent
        else:
            processes.append(pid)
            os.close(stdout_pipe[1])
            if stdin:
                os.close(stdin)
            last_out = os.read(stdout_pipe[0], 4096).decode()
            os.close(stdout_pipe[0])
            

    return last_out

commands = [
        ['echo', 'zsh'],
        ['which'],
]

output = run_commands_with_pipes(commands)
print(output)
