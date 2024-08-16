import signal
import os
import sys
import shlex
from myErrors import *


# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)


def parseInput(data: shlex) -> (str, [str], [str]):
    """returns (command, args, flags)"""

    tokens = []
    token = ""

    while True:
        token = data.get_token()
        if (token == None):
            break
        tokens.append(token)

    
    command, args = tokens[0].lower(), tokens[1:]

    return command, args


def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()



    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">>"

    while True:
        try:
            loop(prompt)
        except KeyboardInterrupt:
            print()
            continue
        except myExit as e:
            os._exit(e.code)
        except EOFError as e:
            #TODO: not completely sure if this is right
            os._exit(0)


def loop(prompt):
    while True:
        data = input(f"{prompt} ")
        tokens = shlex.shlex(data, posix = True)
        tokens.escapedquotes = "'\""

        try:
            command, args = parseInput(tokens)
        except ValueError as e:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")
            continue

        if command == "exit":
            raise myExit(0)


if __name__ == "__main__":
    main()
