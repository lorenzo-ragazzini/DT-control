from typing import Callable

class DecisionVariables(dict):
    def __init__(self, *args, **kwargs):
        self._callback:Callable = None
        super().__init__(*args, **kwargs)
    def set_callback(self, callback):
        self._callback = callback
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        if self.get(key) != value:
            super().__setitem__(key, value)
            if self._callback:
                self._callback()

if __name__ == '__main__':
    a = DecisionVariables()
    a['a']=1