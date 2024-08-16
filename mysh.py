import signal
import os
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


def parseInput(data: str) -> (str, [str], [str]):
    """returns (command, args, flags)"""
    data = data.split()
    command, data = data[0].lower(), data[1:]

    args = []
    flags = []

    for item in data:
        if item.startswith("-"):
            flags.append(item)
        else: 
            args.append(item)

    return command, args, flags


def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()



    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">>"

    while True:
        try:
            loop(prompt)
        except KeyboardInterrupt:
            continue
        except myExit as e:
            os._exit(e.code)
        except EOFError as e:
            #TODO: not completely sure if this is right
            os._exit(0)


def loop(prompt):
    while True:
        data = input(f"{prompt} ")
        command, args, flags = parseInput(data)

        if command == "exit":
            raise myExit(0)


if __name__ == "__main__":
    main()
