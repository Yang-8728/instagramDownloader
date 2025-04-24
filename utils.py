# utils.py
import os
import sys
from contextlib import contextmanager

@contextmanager
def suppress_stdout_stderr():
    """Suppress all stdout/stderr during instaloader operations"""
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = devnull
            sys.stderr = devnull
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
