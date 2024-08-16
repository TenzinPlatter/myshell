import os

def main():
    if not (prompt := os.environ.get("PROMPT")):
        prompt = ">> "

    while True:
        command = input(f"{prompt} ")


if __name__ == "__main__":
    main()
