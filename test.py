import signal

def kill_handler(x, y):
    print("I can't be killed, ha ha")
signal.signal(signal.SIGT, kill_handler)

while(True):
    pass
