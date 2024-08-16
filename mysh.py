import os

class myExit(Exception):
    def __init__(self, errorCode):
        self.code = errorCode

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

def main():
    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">> "

    while True:
        try:
            loop(prompt)
        except KeyboardInterrupt:
            continue
        except myExit as e:
            os._exit(e.code)


def loop(prompt):
    while True:
        data = input(f"{prompt} ")
        command, args, flags = parseInput(data)

        if command == "exit":
            raise myExit(0)



if __name__ == "__main__":
    main()
