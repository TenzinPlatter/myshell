import signal
import os
import sys
import shlex
import settings
from myErrors import *
from command import run_command
import myParsing

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)


def main() -> None:
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
        except EOFError as e:
            #TODO: not completely sure if this is right
            print()
            os._exit(0)

def loop():
    while True:
        prompt = settings.get_var("prompt")
        data = input(f"{prompt} ")
        try:
            args = myParsing.get_tokens_list(data)
            if (len(args) < 1):
                continue
            command = args[0]
            result = run_command(args)
            if result is None:
                continue
            else:
                print(result)

        except ValueError as e:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")

        except errorMsg as e:
            sys.stderr.write(e.msg + "\n")

if __name__ == "__main__":
    main()
