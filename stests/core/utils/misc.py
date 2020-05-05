import time


class Timer(object):
    """Timer context manager.
    
    """
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args, **kwargs):
        self.elapsed = time.time() - self.start
