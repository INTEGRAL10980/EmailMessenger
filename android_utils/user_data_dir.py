import os

class Dir:
    """ A special class. It serves to combine relative paths with an absolute one """
    def __init__(self, path : str) -> None:
        self.path = path
    def __mul__(self, path : str) -> str:
        return os.path.join(self.path, path)