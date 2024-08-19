import signal
import os
import sys
import shlex
from myErrors import *
from command import run_command


# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)

# def run_command(command, args):



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

def get_tokens_obj(prompt):
    data = input(f"{prompt} ")
    tokens = shlex.shlex(data, posix = True)
    tokens.escapedquotes = "'\""
    tokens.wordchars += "-./"
    return tokens

def loop(prompt):
    while True:
        tokens_obj = get_tokens_obj(prompt)
        try:
            args = [token for token in tokens_obj]
            command = args[0]
            if (len(args) < 1):
                continue
            print(args)
            run_command(args)

        except ValueError as e:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")
            continue

        except errorMsg as e:
            sys.stderr.write(e.msg)

        if command == "exit":
            raise myExit(0)


if __name__ == "__main__":
    main()
