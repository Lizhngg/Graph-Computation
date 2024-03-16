import os

def mkdir(*args: str) -> tuple:
    for path in args:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    return args