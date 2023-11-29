from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from itertools import chain
from .controlRule import ControlRule

class ControlMap(ABC):
    def __init__(self) -> None:
        self.rules:List[ControlRule] = list()
        self._controller = None
    def __call__(self,event):
        return list(chain(*[rule(event) for rule in self.rules]))
'''
class ControlMap(ABC):
    rules:Dict[str,ControlRule]
    def __call__(self,event):
        for key in self.rules:
            self.rules[key](event)
'''
