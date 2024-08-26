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

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)


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
        except KeyboardInterrupt:
            print()
            continue
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
            if len(args) < 1:
                continue

            result = run_command(args)
            if result is None:
                continue

            print(result)

        except ValueError:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")

        except ErrorMsg as e:
            sys.stderr.write(e.msg + "\n")

if __name__ == "__main__":
    main()
