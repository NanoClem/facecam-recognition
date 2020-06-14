import os


def pathExists(func):
    def wrapper_func(*args, **kwargs):
        if os.path.isdir(args[0]) or os.path.isfile(args[0]):
            return func(*args, **kwargs)
        else: 
            raise OSError("file or directory not found")
    return wrapper_func