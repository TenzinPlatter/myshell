"""
Main program file, shell can be run by running this file with python
"""

import signal
import os
import sys
import settings
from my_errors import ErrorMsg
from command import run_command
import parsing

def handle_interrupt(*_):
    """
    Handle keyboard interrupt with newline
    """
    print()

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    signal.signal(signal.SIGINT, handle_interrupt)


def main() -> None:
    """
    Main function
    Has infinite loop for user shell input
    """
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()

    # sets cwd and prompt
    settings.init()

    while True:
        try:
            loop()
        except EOFError:
            print()
            os._exit(0)

def loop():
    """
    Main loop for handling user input can exit when encountering an error, is 
    recalled by main function
    """
    while True:
        prompt = settings.get_var("PROMPT")
        data = input(prompt)

        try:
            args = parsing.get_tokens(data)
        except ValueError:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")
            continue
        except ErrorMsg as e:
            sys.stderr.write(e.msg + "\n")
            continue

        if len(args) < 1:
            continue

        try:
            # checks if there is a pipe passed in outside of quotes
            result = run_command(args)
        except ErrorMsg as e:
            sys.stderr.write(e.msg + "\n")
            continue

        if result is None:
            continue

        sys.stdout.write(result)

if __name__ == "__main__":
    main()
