debug = False

def set_debug_mode(flag: bool):
    debug = flag

def log(msg: str):
    if debug is True:
        print(msg)