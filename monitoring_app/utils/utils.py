import sys
import select

def wait_for_enter(timeout=0):
    if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
        line = sys.stdin.readline()
        if line.strip() == "" or line.strip() == "\n":
            return True
    return False

