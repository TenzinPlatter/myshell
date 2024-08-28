import os
import signal
import sys

def run_commands_with_pipes(command_list):
    processes = []
    
    # Set up a signal handler to terminate all processes on Ctrl+C
    def signal_handler(*_):
        for process in processes:
            try:
                os.kill(process, signal.SIGTERM)
            except ProcessLookupError:
                pass
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    # File descriptors for the previous process's output (initially None)
    prev_fd = None
    
    for i, command in enumerate(command_list):
        if i == len(command_list) - 1:
            # Last command, we will capture its output
            stdout = os.pipe()[1] if prev_fd else None
        else:
            # Create a pipe for the next command
            next_fd = os.pipe()
            stdout = next_fd[1]
        
        # Fork the process
        pid = os.fork()
        
        if pid == 0:  # Child process
            if prev_fd is not None:
                os.dup2(prev_fd, 0)  # Set previous process's output as input
                os.close(prev_fd)
            if stdout is not None:
                os.dup2(stdout, 1)  # Set next process's input as output
                os.close(stdout)
            
            # Execute the command
            os.execvp(command[0], command)
        else:  # Parent process
            processes.append(pid)
            if prev_fd is not None:
                os.close(prev_fd)
                prev_fd = -1
            if stdout is not None:
                os.close(stdout)
            if i < len(command_list) - 1:
                prev_fd = next_fd[0]  # Set for the next command's input
    
    # Capture and return the output of the last command
    if prev_fd is not None:
        result = os.read(prev_fd, 4096)
        os.close(prev_fd)
        return result.decode()

# Example usage
commands = [
    ['echo', 'Hello, World!'],
    ['tr', 'a-z', 'A-Z'],
    ['rev']
]

output = run_commands_with_pipes(commands)
print("Final Output:", output)
