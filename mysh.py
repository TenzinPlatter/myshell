import signal
import os
import sys
import shlex
import vars
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

def get_tokens_obj(data):
    tokens = shlex.shlex(data, posix = True)
    tokens.escapedquotes = "'\""
    tokens.wordchars += "-./"
    return tokens

def get_tokens_list(tokens_obj):
    args = [token for token in tokens_obj]
    for i in range(len(args)):
        if args[i].startswith("${") and args[i].endswith("}"):
            args[i] = vars.get(args[i][2:-1])
    return args

def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()

    # sets cwd and prompt
    vars.init()

    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print()
            continue
        except EOFError as e:
            #TODO: not completely sure if this is right
            os._exit(0)

def loop():
    while True:
        prompt = vars.get("prompt")
        data = input(f"{prompt} ")
        try:
            tokens_obj = get_tokens_obj(data)
            args = get_tokens_list(tokens_obj)
            if (len(args) < 1):
                continue
            command = args[0]
            run_command(args)

        except ValueError as e:
            sys.stderr.write("mysh: syntax error: unterminated quote\n")

        except errorMsg as e:
            sys.stderr.write(e.msg)

if __name__ == "__main__":
    main()
