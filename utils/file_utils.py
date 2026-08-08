import os

def cleanup(files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)